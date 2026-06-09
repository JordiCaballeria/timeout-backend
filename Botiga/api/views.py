from rest_framework import viewsets
from .serializers import *

class TallesViewSet(viewsets.ModelViewSet):
    queryset = Talles.objects.all()
    serializer_class = TallesSerializer

class TipusProducteViewSet(viewsets.ModelViewSet):
    queryset = TipusProducte.objects.all()
    serializer_class = TipusProducteSerializer

class ProducteViewSet(viewsets.ModelViewSet):
    queryset = Producte.objects.all()
    serializer_class = ProducteSerializer

class ProducteTallesViewSet(viewsets.ModelViewSet):
    queryset = ProducteTalles.objects.all()
    serializer_class = ProducteTallesSerializer

class TipusPagamentViewSet(viewsets.ModelViewSet):
    queryset = TipusPagament.objects.all()
    serializer_class = TipusPagamentSerializer
class PagamentViewSet(viewsets.ModelViewSet):
    queryset = Pagament.objects.all()
    serializer_class = PagamentSerializer

class EntradaViewSet(viewsets.ModelViewSet):
    queryset = Entrada.objects.all()
    serializer_class = EntradaSerializer

class DetallsPagamentViewSet(viewsets.ModelViewSet):
    queryset = DetallsPagament.objects.all()
    serializer_class = DetallsPagamentSerializer

class ImatgesProducteViewSet(viewsets.ModelViewSet):
    queryset = ImatgesProducte.objects.all()
    serializer_class = ImatgesProducteSerializer

class EnviamentViewSet(viewsets.ModelViewSet):
    queryset = Enviament.objects.all()
    serializer_class = EnviamentSerializer

class EstatEnviamentViewSet(viewsets.ModelViewSet):
    queryset = EstatEnviament.objects.all()
    serializer_class = EstatEnviamentSerializer



