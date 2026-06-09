from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView

from TimeOut import settings
from TimeOut.permisos import *
from User.api.serializers import UserSerializer, RolSerializer, RolUsuariSerializer, PermisosSerializer, \
    RegisterSerializer, UserSerializer3

from User.models import *


class UserApiViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        request.data['password'] = make_password(request.data['password'])
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        password = request.data['password']
        if password:
            request.data['password'] = make_password(password)
        else:
            request.data['password'] = request.user.password

        return super().update(request, *args, **kwargs)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer3(request.user, context={'request': request})
        return Response(serializer.data)


class JugadoresView(APIView):
    permission_classes = [IsAuthenticated, HasVeureJugadorsPermission]

    def get(self, request):
        # Consulta a la base de datos para obtener los usuarios que tienen el rol "Jugador/a"
        jugadores = User.objects.filter(rols__nom='Jugador/a')

        # Serializar los usuarios utilizando el UserSerializer2
        serializer = UserSerializer3(jugadores, context={'request': request}, many=True)
        return Response(serializer.data)


class UserPhotoUpdateAPIView(APIView):

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


        user.path_photo = request.data.get('path_photo', user.path_photo)
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RolApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, HasVeureRolsPermission]
    serializer_class = RolSerializer
    queryset = Rol.objects.all()


class RolUsuariApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RolUsuariSerializer
    queryset = RolUsuari.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rol', 'user']


class PermisosApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PermisosSerializer
    queryset = Permisos.objects.all()


class RegistrationView(APIView):
    def post(self, request):
        # Obtenim l'adreça de correu electrònic de la petició
        email = request.data.get('email')

        # Comprovem si l'usuari ja existeix en la base de dades a través del seu correu electrònic
        if User.objects.filter(email=email).exists():
            # Si l'usuari ja existeix, enviem un missatge d'error indicant que el correu electrònic ja està vinculat a un usuari
            error_message = {'error': 'El email ja està vinculat a un usuari.'}
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        # Si l'usuari no existeix, procedim amb el registre
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Si les dades són vàlides, desem l'usuari i enviem un correu electrònic d'activació
            user = serializer.save()

            # Generem el token d'activació per a l'usuari i construïm l'enllaç d'activació
            activation_token = user.generate_activation_token()
            activation_link = request.build_absolute_uri(reverse('activate-user', args=[user.pk, activation_token]))

            # Construïm el cos del correu electrònic amb les dades de l'usuari i l'enllaç d'activació
            context = {'username': user.username, 'activation_link': activation_link}
            email_subject = 'Activació del teu compte'
            email_body = render_to_string('activate-user.html', context)

            # Enviem el correu electrònic d'activació a l'usuari
            email = EmailMessage(
                email_subject, email_body, settings.EMAIL_HOST_USER, [user.email])
            email.content_subtype = 'html'
            email.send()

            # Retornem una resposta satisfactòria amb les dades de l'usuari registrat
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Si les dades no són vàlides, enviem un missatge d'error indicant que l'usuari ja existeix
        error_message = {'error': 'L\'usuari que has triat ja està en ús.'}
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


class ActivateUserView(APIView):
    def get(self, request, pk, token):
        try:
            user = User.objects.get(pk=pk, activation_token=token)
        except User.DoesNotExist:
            # Si no es troba cap usuari amb l'ID i el token d'activació proporcionats, es retorna un missatge d'error
            return Response({'error': 'Enllaç d\'activació no vàlid'}, status=status.HTTP_400_BAD_REQUEST)

        # Activem l'usuari establint l'estat "is_active" a True i eliminant el token d'activació
        user.is_active = True
        user.activation_token = None
        user.save()

        # Renderitzem la plantilla account_activated.html per mostrar un missatge de confirmació a l'usuari
        return render(request, 'account_activated.html')


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Obtiene los datos de la respuesta
        data = response.data

        # Obtiene el usuario a partir del nombre de usuario proporcionado en la solicitud
        user = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )

        # Verifica si el usuario existe y si su cuenta está activa
        if user and not user.is_active:
            data['error'] = 'La cuenta no está activa'
            del data['access']
            del data['refresh']
            return JsonResponse(data, status=403)

        return response
