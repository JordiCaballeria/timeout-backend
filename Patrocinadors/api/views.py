from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from Patrocinadors.api.serializers import PatrocinadorsSerializer
from Patrocinadors.models import Patrocinador



class patorcinadorsApiViewSet(ModelViewSet):
    serializer_class = PatrocinadorsSerializer
    queryset = Patrocinador.objects.all()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def public_detail(self, request, pk=None):
        patrocinador = self.get_object()
        serializer = self.get_serializer(patrocinador)
        return Response(serializer.data)