from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from Esdeveniment.models import Esdeveniment, TipusEsdeveniment
from Esdeveniment.api.serializers import EsdevenimentSerializer, TipusEsdevenimentSerializer
from django_filters.rest_framework import DjangoFilterBackend

from TimeOut.permisos import HasVeureEsdevenimentsPermission


class EsdevenimentApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, HasVeureEsdevenimentsPermission]
    serializer_class = EsdevenimentSerializer
    queryset = Esdeveniment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tipusEsdeveniment']

class TipusEsdevenimentApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, HasVeureEsdevenimentsPermission]
    serializer_class = TipusEsdevenimentSerializer
    queryset = TipusEsdeveniment.objects.all()