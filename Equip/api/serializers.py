from rest_framework import serializers
from Equip.models import Equip, Divisio, Esport, Categoria, EquipUsuaris
from User.api.serializers import RolUsuariSerializer
from Esdeveniment.api.serializers import EsdevenimentSerializer


class DivisioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Divisio
        fields = '__all__'


class EsportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Esport
        fields = '__all__'


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class EquipsSerializer(serializers.ModelSerializer):
    users_data = RolUsuariSerializer(source='users', many=True, read_only=True)
    divisio_data = DivisioSerializer(source='divisio', read_only=True)
    categoria_data = CategoriaSerializer(source='categoria', read_only=True)
    esport_data = EsportSerializer(source='esport', read_only=True)
    esdeveniments = EsdevenimentSerializer(many=True, read_only=True)

    class Meta:
        model = Equip
        fields = ['id', 'nom', 'divisio', 'esport', 'categoria', 'created_at', 'esport_data', 'categoria_data',
                  'divisio_data', 'users_data', 'esdeveniments']


class EquipUsuarisSerializer(serializers.ModelSerializer):
    rolusuari_data = RolUsuariSerializer(source='rolusuari', read_only=True)
    equip_data = EquipsSerializer(source='equip', read_only=True)

    class Meta:
        model = EquipUsuaris
        fields = ['id', 'rol', 'user', 'rol_data', 'user_data']


class EquipsSerializer2(serializers.ModelSerializer):
    divisio_data = DivisioSerializer(source='divisio', read_only=True)
    categoria_data = CategoriaSerializer(source='categoria', read_only=True)
    esport_data = EsportSerializer(source='esport', read_only=True)
    esdeveniments = EsdevenimentSerializer(many=True, read_only=True)

    class Meta:
        model = Equip
        fields = ['id', 'nom', 'created_at', 'esport_data', 'categoria_data', 'divisio_data', 'esdeveniments']
