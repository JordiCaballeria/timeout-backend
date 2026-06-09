from datetime import date

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Equip.api.serializers import EquipsSerializer
from Equip.models import Equip
from .api.serializers import EsdevenimentSerializer
from .models import Esdeveniment


@api_view(['GET'])
def esdeveniment_partit(request):
    esdeveniments = Esdeveniment.objects.filter(tipusEsdeveniment__nom__icontains='Partit')
    serializer = EsdevenimentSerializer(esdeveniments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def equipsclient(request):
    equips = Equip.objects.all()
    serializer = EquipsSerializer(equips, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def esdeveniments_avui(request):
    esdeveniments = Esdeveniment.objects.filter(data__date=date.today())

    serializer = EsdevenimentSerializer(esdeveniments, many=True)
    return Response(serializer.data)