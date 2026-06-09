from django.test import TestCase
from User.models import User
from django.utils import timezone
from datetime import timedelta

from User.views import desactivar_socis
from django.core import mail
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class DesactivarSocisTestCase(TestCase):
    def setUp(self):
        # Crear usuaris de prova
        self.soci1 = User.objects.create_user(username='soci1', date_finish_soci=timezone.now() - timedelta(days=1),
                                              is_soci=True, email='user_test@example.com')
        self.soci2 = User.objects.create_user(username='soci2', date_finish_soci=timezone.now() + timedelta(days=1),
                                              is_soci=True, email='user_test1@example.com')
        self.noSoci = User.objects.create_user(username='noSoci', date_finish_soci=timezone.now() - timedelta(days=1),
                                               is_soci=False, email='user_test2@example.com')

    def test_desactivar_socis(self):
        # Trucar la funció que vols provar
        desactivar_socis()

        # Verificar que els socis vençuts s'hagin desactivat correctament
        self.soci1.refresh_from_db()
        self.assertFalse(self.soci1.is_soci)

        self.soci2.refresh_from_db()
        self.assertTrue(self.soci2.is_soci)

        self.noSoci.refresh_from_db()
        self.assertFalse(self.noSoci.is_soci)


class EnviarContacteTestCase(APITestCase):
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_enviar_contacte(self):
        url = reverse('enviar_contacte')

        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'poblacio': 'Barcelona',
            'telefon': '123456789',
            'comentaris': 'Missatge de prova',
        }

        response = self.client.post(url, data, format='json')

        # Verificar que el correu electrònic s'ha enviat correctament
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Formulario de contacto')
        self.assertEqual(mail.outbox[0].from_email, 'from@example.com')
        self.assertEqual(mail.outbox[0].to, ['sabrugbyclub@gmail.com'])

        # Verificar la resposta d'èxit de la vista
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Correo electrónico enviado'})
