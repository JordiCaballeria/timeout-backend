from rest_framework.serializers import ModelSerializer

from Esdeveniment.models import Esdeveniment, TipusEsdeveniment
from Equip.api.serializers2 import EquipsSerializer2

class TipusEsdevenimentSerializer(ModelSerializer):
    class Meta:
        model = TipusEsdeveniment
        fields = ['id','nom','descripcio']
class EsdevenimentSerializer(ModelSerializer):
    tipusesdeveniment_data = TipusEsdevenimentSerializer(source='tipusEsdeveniment', read_only=True)
    equip_data = EquipsSerializer2(source='equip', read_only=True)
    class Meta:
        model = Esdeveniment
        fields = '__all__'
        extra_fields = ['equip_data', 'tipusesdeveniment_data']

