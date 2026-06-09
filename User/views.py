from datetime import datetime, timedelta
import json

import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import requests
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.mail import get_connection, EmailMultiAlternatives, EmailMessage
import base64
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

from Botiga.api.serializers import DetallsPagamentSerializer, EntradaSerializer
from Botiga.models import TipusPagament, Pagament, DetallsPagament, Entrada
from TimeOut import settings
from TimeOut.permisos import HasEnviarMailsPermission
from TimeOut.settings import EMAIL_HOST_USER
from .api.serializers import UserSerializer2, UserSerializer
from .models import Rol, User, RolUsuari
import stripe
import os
from stripe import error


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def actualizar_roles(request):
    # Obtener la ID de usuario proporcionada en la solicitud
    user_id = request.data.get('user_id')

    # Obtener el usuario con la ID proporcionada
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado.'}, status=404)

    # Obtener los roles existentes para ese usuario
    roles_actuales = user.rols.all()

    # Obtener los IDs de roles proporcionados en el array
    roles_nuevos = request.data.get('rols')

    # Convertir los IDs a objetos Rol
    roles_nuevos_objs = Rol.objects.filter(id__in=roles_nuevos)

    # Crear un array de IDs de los roles actuales
    roles_actuales_ids = [rol.id for rol in roles_actuales]

    # Crear un array de IDs de los roles nuevos
    roles_nuevos_ids = [rol.id for rol in roles_nuevos_objs]

    # Comparar los arrays y hacer los cambios necesarios en la base de datos
    for rol_id in roles_nuevos_ids:
        if rol_id not in roles_actuales_ids:
            rol = Rol.objects.get(id=rol_id)
            RolUsuari.objects.create(user=user, rol=rol)

    for rol_id in roles_actuales_ids:
        if rol_id not in roles_nuevos_ids:
            rol = Rol.objects.get(id=rol_id)
            RolUsuari.objects.filter(user=user, rol=rol).delete()

    # Retornar una respuesta con éxito
    return JsonResponse({'success': True})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def entrenadores(request):
    # Consulta a la base de datos para obtener los usuarios que tienen el rol "Jugador/a"
    entrenadores = User.objects.filter(rols__nom='Entrenador/a')

    # Serializar los usuarios utilizando el UserSerializer2
    serializer = UserSerializer2(entrenadores, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasEnviarMailsPermission])
def enviar_email(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        user_ids = json_data.get('user_ids', [])
        subject = json_data.get('subject', '')
        message = json_data.get('message', '')
        from_email = 'sabrugbyclub@gmail.com'

        users = User.objects.filter(id__in=user_ids)
        messages = []
        for user in users:
            if user.email:
                # Obtener el mensaje con formato HTML
                html_message = json_data.get('html_message', '')
                # Renderizar el template con los datos necesarios

                # Crear el mensaje con formato HTML y agregarlo a la lista de mensajes
                msg = EmailMultiAlternatives(subject, message, from_email, [user.email])
                msg.attach_alternative(html_message, "text/html")
                messages.append(msg)

        if messages:
            # Envía los mensajes
            connection = get_connection()  # Obtener una conexión de email
            connection.send_messages(messages)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'No valid emails found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid method'})


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


# Crear el valor del hash per generar el token de restabliment de contrasenya.
# S'utilitza l'ID de l'usuari, el timestamp i l'estat d'activació de l'usuari.
# Això assegura que el token sigui únic i estigui vincul

@api_view(['POST'])
def password_reset_request(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        email = json_data.get('email')
        user = User.objects.filter(email=email).first()

        if user is not None:
            token = PasswordResetTokenGenerator().make_token(user)  # Generem el token amb la nostra funció
            domain = f"{request.scheme}://{get_current_site(request).domain}"  # creem enllaç
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            mail_subject = 'Restabliment de contrasenya.'

            # Preparar el context per al correu electrònic de restabliment de contrasenya
            context = {'user': user,
                       'domain': domain,
                       'uid': uid,
                       'token': token, }
            message = render_to_string('password_reset_email.html', context)
            email = EmailMessage(
                mail_subject, message, settings.EMAIL_HOST_USER, [email]
            )
            email.content_subtype = 'html'
            email.send()

            # Resposta d'èxit
            response = {
                'msg': 'S\'ha enviat un correu electrònic de restabliment de contrasenya. Revisi la seva safata d\'entrada.'
            }
            return JsonResponse(response)
        else:
            # Resposta d'error
            response = {
                'error': 'No s\'ha trobat cap compte amb aquesta adreça de correu electrònic.'
            }
            return JsonResponse(response, status=400)


# Afegim la api key privada del nostre compte stripe a la variable stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', '')

@api_view(['POST'])
def pagament_stripe(request):
    if request.method == 'POST':
        payment_method_id = request.data.get('payment_method_id')
        amount = request.data.get('amount')

        try:
            # Crear un pagament en Stripe a traves de api stripe
            stripe.PaymentIntent.create(
                amount=amount,
                currency='eur',
                payment_method=payment_method_id,
                confirm=True,
            )

            return JsonResponse({'success': True})
        except stripe.error.CardError as e:
            # Si la targeta és rebutjada, retornar un missatge d'error
            return JsonResponse({'success': False, 'error': e.user_message})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def nou_soci(request):
    user_id = request.data.get('user_id')
    anys = int(request.data.get('anys'))
    preu = request.data.get('total')
    tipusPagament_id = request.data.get('tipusPagament_id')
    user = get_object_or_404(User, id=user_id)
    user.is_soci = True
    user.date_finish_soci = datetime.now() + timedelta(days=365 * anys)
    user.date_joined_soci = datetime.now()
    user.save()

    tipusPagament = get_object_or_404(TipusPagament, id=tipusPagament_id)

    pagament = Pagament.objects.create(user=user, total=preu, tipuspagament=tipusPagament)
    pagament.save()

    return Response({"message": "El soci i el pagament s'han creat de manera satisfactoria"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def resum(request):
    if not (request.user.is_staff):
        return Response("No tens permisos")
    ultims_users = User.objects.filter(date_joined__isnull=False).order_by('-date_joined')[:10]
    ultims_soci_users = User.objects.filter(date_joined_soci__isnull=False, is_soci=True).order_by('-date_joined_soci')[
                        :10]
    ultims_productesvenuts = DetallsPagament.objects.filter(id__isnull=False).order_by('-id')[:10]
    ultimes_entradesvenudes = Entrada.objects.filter(id__isnull=False).order_by('-id')[:10]

    user_serializer = UserSerializer(ultims_users, many=True)
    soci_user_serializer = UserSerializer(ultims_soci_users, many=True)
    detallspagament_serializer = DetallsPagamentSerializer(ultims_productesvenuts, many=True)
    entrades_serializer = EntradaSerializer(ultimes_entradesvenudes, many=True)

    response_data = {
        'ultims_users': user_serializer.data,
        'ultims_soci_users': soci_user_serializer.data,
        'ultims_productesvenuts': detallspagament_serializer.data,
        'ultimes_entradesvenudes': entrades_serializer.data,
    }

    return Response(response_data)


@api_view(['POST'])
def enviar_contacte(request):
    # Obtener los datos del formulario del cuerpo de la solicitud
    form_data = request.data

    # Validar los datos del formulario si es necesario
    # ...

    # Crear el cuerpo del correo electrónico utilizando un template
    context = {
        'first_name': form_data.get('first_name'),
        'last_name': form_data.get('last_name'),
        'email': form_data.get('email'),
        'poblacio': form_data.get('poblacio'),
        'telefon': form_data.get('telefon'),
        'comentaris': form_data.get('comentaris'),
    }
    email_body = render_to_string('contacte_template.html', context)

    # Crear el objeto EmailMessage
    email = EmailMessage(
        subject='Formulario de contacto',
        body=email_body,
        from_email='from@example.com',  # Remitente del correo electrónico
        to=['sabrugbyclub@gmail.com'],  # Destinatario(s) del correo electrónico
    )
    email.content_subtype = 'html'  # Indicar que el contenido del correo es HTML

    # Enviar el correo electrónico
    email.send()

    # Responder con una respuesta de éxito
    return Response({'message': 'Correo electrónico enviado'})


def desactivar_socis():
    socios_vencidos = User.objects.filter(date_finish_soci__lt=timezone.now(), is_soci=True)
    for socio in socios_vencidos:
        socio.is_soci = False
        socio.save()
