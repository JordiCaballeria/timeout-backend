from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from Esdeveniment.models import Esdeveniment
from Esdeveniment.api.serializers import EsdevenimentSerializer
from User.models import User


class EsdevenimentsAvuiTestCase(APITestCase):
    def setUp(self):
        # Crea un usuari de prova
        self.user = User.objects.create_user(username='user_test', email='user_test@example.com',
                                             password='test_password')

        # Crea alguns objectes Esdeveniment para el día actual
        self.esdeveniment1 = Esdeveniment.objects.create(nom="Esdeveniment 1", data=date.today())
        self.esdeveniment2 = Esdeveniment.objects.create(nom="Esdeveniment 2", data=date.today())
        self.esdeveniment3 = Esdeveniment.objects.create(nom="Esdeveniment 3", data=date.today())

        # Crea un objecte Esdeveniment per a un altre día
        Esdeveniment.objects.create(nom="Esdeveniment altre día", data=date(2024, 5, 19))

    def test_esdeveniments_avui(self):
        url = reverse('esdeveniments_avui')

        # Autenticar l'usuari par les proves
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Obte els objectes Esdeveniment filtrats pel día actual
        esdeveniments = Esdeveniment.objects.filter(data__date=date.today())
        serializer = EsdevenimentSerializer(esdeveniments, many=True)

        self.assertEqual(response.data, serializer.data)