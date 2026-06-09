from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from Equip.models import Equip, Divisio, Esport, Categoria, EquipUsuaris
from Equip.api.serializers import EquipsSerializer, DivisioSerializer, EsportSerializer, CategoriaSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import  IsAuthenticated, AllowAny

from TimeOut.permisos import *


class EquipApiViewSet(ModelViewSet):
    serializer_class = EquipsSerializer
    queryset = Equip.objects.all()
    permission_classes = [IsAuthenticated, HasVeureEquipsPermission]


class EquipsApiView(APIView):
    permission_classes = [HasVeureEquipsPermission]

    def get(self, request):
        serializer = EquipsSerializer(request.equip)
        return Response(serializer.data)

class DivisioApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, HasVeureCompeticioPermission]
    serializer_class = DivisioSerializer
    queryset = Divisio.objects.all()
class DivisioApiView(APIView):
    permission_classes = [IsAuthenticated, HasVeureCompeticioPermission]
    def get(self, request):
        serializer = DivisioSerializer(request.divisio)
        return Response(serializer.data)

class EsportApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, HasVeureCompeticioPermission]
    serializer_class = EsportSerializer
    queryset = Esport.objects.all()
class EsportApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = EsportSerializer(request.divisio)
        return Response(serializer.data)

class CategoriaApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, HasVeureCompeticioPermission]
    serializer_class = CategoriaSerializer
    queryset = Categoria.objects.all()
class CategoriaApiView(APIView):
    permission_classes = [IsAuthenticated, HasVeureCompeticioPermission]
    def get(self, request):
        serializer = CategoriaSerializer(request.divisio)
        return Response(serializer.data)

