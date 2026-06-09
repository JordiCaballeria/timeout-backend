import string
import random

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Esdeveniment.models import Esdeveniment
from TimeOut.permisos import HasEditarEntradesPermission
from TimeOut.utils import generate_qr_code
from User.models import User
from .models import Producte, ImatgesProducte, Talles, ProducteTalles, Entrada
from Botiga.api.serializers import ProducteSerializer, ImatgesProducteSerializer, PagamentSerializer, \
    DetallsPagamentSerializer, TipusPagamentSerializer, EntradaSerializer
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


@api_view(['POST'])
def crear_producte(request):
    # Paso A: Crear el objeto Producte
    producte_serializer = ProducteSerializer(data=request.data.get('producte'))
    if producte_serializer.is_valid():
        producte = producte_serializer.save()
    else:
        return Response(producte_serializer.errors, status=400)
    producte_id = producte.id
    # Paso C: Crear los objetos ProducteTalles
    talles = request.data.get('talles', {})
    for talla_id, quantitat in talles.items():
        talla = Talles.objects.get(id=talla_id)
        producte_talla = ProducteTalles(talla=talla, producte=producte, quantitat=quantitat)
        producte_talla.save()

    return Response({'id': producte_id, 'message': 'El producto ha sido creado exitosamente.'})


@api_view(['POST'])
def actualitzar_producte(request):
    producte_data = request.data.get('producte')
    producte_id = request.data.get('producte_id')
    imatges = request.data.get('imatges')
    talles_data = request.data.get('talles')

    producte = get_object_or_404(Producte, pk=producte_id)

    # Actualizar datos del producto
    producte.preu = producte_data.get('preu', producte.preu)
    producte.preu_soci = producte_data.get('preu_soci', producte.preu_soci)
    producte.nom = producte_data.get('nom', producte.nom)
    producte.descripcio = producte_data.get('descripcio', producte.descripcio)
    producte.tipusProducte_id = producte_data.get('tipusProducte', producte.tipusProducte_id)
    producte.actiu = producte_data.get('actiu', producte.actiu)
    producte.save()

    # Actualizar datos de ProducteTalles
    for talla_id, quantitat in talles_data.items():
        talla = get_object_or_404(Talles, pk=talla_id)
        producte_talla, created = ProducteTalles.objects.get_or_create(
            talla=talla,
            producte=producte,
            defaults={'quantitat': quantitat}
        )
        if not created:
            producte_talla.quantitat = quantitat
            producte_talla.save()

    # Eliminar imágenes del producto
    for imatge in imatges:
        imatge_id = imatge.get('id')
        if imatge_id:
            ImatgesProducte.objects.filter(id=imatge_id).delete()

    return Response({'message': 'Producto actualizado correctamente.'})


@api_view(['POST'])
def crear_imatges_producte(request):
    # Obtener la ID del producto del body del request
    producte_id = request.data.get('producte_id')
    print(producte_id)
    # Obtener las imágenes del body del request
    imatges = request.FILES.getlist('imatges[]')
    print(imatges)
    # Crear un registro en la tabla ImatgesProducte por cada imagen recibida
    for imatge in imatges:
        ImatgesProducte.objects.create(
            producte_id=producte_id,
            path_imatge=imatge
        )

    # Devolver una respuesta exitosa
    return Response({'message': 'Imágenes creadas exitosamente.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_pagament(request):
    try:
        user_id = request.data['user_id']
        total = request.data['total']
        tipus_pagament_id = request.data['tipusPagament']['id']  # obtener el id del tipo de pago
        productes_data = request.data['productes']

        # obtener el objeto User correspondiente a user_id
        user = User.objects.get(pk=user_id)

        # crear y guardar el objeto Pagament
        pagament_data = {'user': user.pk, 'total': total,
                         'tipuspagament': tipus_pagament_id}  # usar el id del tipo de pago
        pagament_serializer = PagamentSerializer(data=pagament_data)
        pagament_serializer.is_valid(raise_exception=True)
        pagament = pagament_serializer.save()

        # iterar a través de los objetos de Producte y crear y guardar los objetos DetallsPagament correspondientes
        for producte_data in productes_data:
            # obtener el objeto ProducteTalles correspondiente y actualizar su cantidad
            producte_talla = ProducteTalles.objects.get(pk=producte_data['productetalla_id'])
            producte_talla.quantitat -= producte_data['quantitat']
            producte_talla.save(update_fields=['quantitat'])

            # crear y guardar el objeto DetallsPagament correspondiente
            detalls_pagament_data = {'pagament': pagament.pk, 'producte': producte_data['producte']['id'],
                                     'quantitat': producte_data['quantitat'], 'talla': producte_talla.talla.pk}

            detalls_pagament_serializer = DetallsPagamentSerializer(data=detalls_pagament_data)
            detalls_pagament_serializer.is_valid(raise_exception=True)
            detalls_pagament_serializer.save()

        return Response(pagament_serializer.data)

    except KeyError:
        return Response({'message': 'Faltan datos en la solicitud'}, status=status.HTTP_400_BAD_REQUEST)

    except ObjectDoesNotExist:
        return Response({'message': 'No se encontró el usuario'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vendre_entrades(request):
    # Obtener los datos del request
    user_id = request.data.get('user_id') #Identificador de l'usuari que compra les entrades
    esdeveniment_id = request.data.get('esdeveniment_id') #Identificador del esdeveniment de l'entrada
    quantitat = request.data.get('quantitat') #Quantitat de entrades que compra l'usuari
    tipusPagament_id = request.data.get('tipusPagament_id') #El tipus de pagament amb que realitza la compra
    total = request.data.get('total') #Total del pagament

    # Crear el registre de pagament
    pagament_data = {
        'user': user_id,
        'total': total,
        'tipuspagament': tipusPagament_id,
    }
    #Serialitzar el pagament
    pagament_serializer = PagamentSerializer(data=pagament_data)

    #Comprovar si el pagament es valid
    if not pagament_serializer.is_valid():
        return Response(pagament_serializer.errors, status=400)

    # Crear pagament
    pagament = pagament_serializer.save()

    #Obtenir usuari de la base de dades
    user = User.objects.get(pk=user_id)

    # Crear los registres d'entrada i de codis QR
    entrades = []
    qr_codes = []

    #Establirem les caracteristiques de la cadena de caracters aleatoria que se li assignarà a cada codi QR
    longitud = 50
    caracteres = string.ascii_letters + string.digits + string.punctuation


    #Creem un bucle amb la quanitat de entrades a vendre i creem una cadena aleatoria, un registre d'entrada
    # i un codi qr per cada una de les entrades venudes
    for i in range(quantitat):
        cadena_aleatoria = ''.join(random.choices(caracteres, k=longitud))
        entrada_data = {
            'esdeveniment': esdeveniment_id,
            'pagament': pagament.id,
            'activa': True,
            'codi': cadena_aleatoria
        }
        entrada_serializer = EntradaSerializer(data=entrada_data)
        if not entrada_serializer.is_valid():
            return Response(entrada_serializer.errors, status=400)
        entrada = entrada_serializer.save()
        entrades.append(entrada)

        # Generar el código QR y añadirlo a la lista de códigos QR
        qr_code_buffer = generate_qr_code(f"{entrada.codi}")
        qr_codes.append({
            'id': entrada.id,
            'qr_code': qr_code_buffer.getvalue(),
        })

    # Actualizar el camp num_entrades_disponibles del Esdeveniment
    esdeveniment = Esdeveniment.objects.get(id=esdeveniment_id)
    esdeveniment.num_entrades_disponibles = esdeveniment.num_entrades_disponibles - quantitat
    esdeveniment.save()

    # Crear un missatge de correu electrònic
    subject = f"Entrades per {esdeveniment.nom}"
    from_email = 'sabrugbyclub@gmail.com'
    to_email = user.email
    message = render_to_string('entradestemplate.html', {'entradas': entrades, 'qr_codes': qr_codes})
    msg = EmailMessage(subject, message, from_email, [to_email])
    #Adjuntem al missatge, els codis QR de les entrades
    for qr in qr_codes:
        msg.attach(f"entrada_{qr['id']}.png", qr['qr_code'], "image/png")
    msg.content_subtype = "html"

    # Enviar el correu electònic
    msg.send()
    #Retornem les entrades creades anteriorment serialitzades
    return Response({'entrades': EntradaSerializer(entrades, many=True).data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validar_entrada(request):
    codientrada = request.data.get('codientrada')
    esdevenimentActual = request.data.get('esdevenimentActual')
    print(esdevenimentActual)
    try:
        entrada = Entrada.objects.get(codi=codientrada)
        esdeveniment = Esdeveniment.objects.get(pk=esdevenimentActual)
        print(entrada.esdeveniment)
        print(esdeveniment.nom)
        if entrada.activa:
            if entrada.esdeveniment != esdeveniment:
                mensaje = 'L entrada no es per l esdeveniment actual'
            else:
                entrada.activa = False
                entrada.save()
                mensaje = 'Entrada vàlida'
        else:
            mensaje = 'Entrada ja utilitzada i validada'
    except Entrada.DoesNotExist:
        mensaje = 'Entrada no encontrada'

    return Response({'mensaje': mensaje})