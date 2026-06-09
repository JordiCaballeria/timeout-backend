from rest_framework import serializers
from Equip.models import Equip, Divisio, Esport, Categoria

class DivisioSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Divisio
        fields = '__all__'

class EsportSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Esport
        fields = '__all__'
class CategoriaSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class EquipsSerializer2(serializers.ModelSerializer):
    divisio_data=DivisioSerializer2(source='divisio', read_only=True)
    categoria_data = CategoriaSerializer2(source='categoria', read_only=True)
    esport_data = EsportSerializer2(source='esport', read_only=True)

    class Meta:
        model = Equip
        fields = ['id', 'nom', 'created_at', 'esport_data', 'categoria_data', 'divisio_data']


