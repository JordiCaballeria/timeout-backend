from rest_framework import serializers
from Botiga.models import *
from Esdeveniment.api.serializers import EsdevenimentSerializer
from User.api.serializers import UserSerializer


class TallesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talles
        fields = '__all__'


class TipusProducteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipusProducte
        fields = '__all__'


class ImatgesProducteSerializer2(serializers.ModelSerializer):
    class Meta:
        model = ImatgesProducte
        fields = ('path_imatge',)


class ProducteTallesSerializer(serializers.ModelSerializer):
    talla = TallesSerializer()

    class Meta:
        model = ProducteTalles
        fields = '__all__'
        extra_fields = ['talla']


class ProducteSerializer(serializers.ModelSerializer):
    imatges_producte = serializers.SerializerMethodField()
    talles_producte = ProducteTallesSerializer(source='productetalles_set', many=True, read_only=True)
    tipus_data = TipusProducteSerializer(source='tipusProducte', read_only=True)
    class Meta:
        model = Producte
        fields = '__all__'
        extra_fields = ['imatges_producte', 'talles_producte', 'tipus_data']

    def get_imatges_producte(self, obj):
        imatges = ImatgesProducte.objects.filter(producte=obj)
        return ImatgesProducteSerializer(imatges, many=True).data


class ImatgesProducteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImatgesProducte
        fields = '__all__'


class TipusPagamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipusPagament
        fields = '__all__'

class PagamentSerializer2(serializers.ModelSerializer):
    user_data = UserSerializer(source='user', read_only=True)
    tipuspagament_data = TipusPagamentSerializer(source='tipuspagament', read_only=True)
    class Meta:
        model = Pagament
        fields = '__all__'
        extra_fields = ['user_data', 'tipuspagament_data', 'detalls_data']
class DetallsPagamentSerializer(serializers.ModelSerializer):
    producte_data = ProducteSerializer(source='producte', read_only=True)
    pagament_data = PagamentSerializer2(source='pagament',read_only=True)
    talla_data = TallesSerializer(source='talla', read_only=True)

    class Meta:
        model = DetallsPagament
        fields = '__all__'


class PagamentSerializer(serializers.ModelSerializer):
    user_data = UserSerializer(source='user', read_only=True)
    tipuspagament_data = TipusPagamentSerializer(source='tipuspagament', read_only=True)
    detalls_data = DetallsPagamentSerializer(source='detallspagament_set', read_only=True, many=True)

    class Meta:
        model = Pagament
        fields = '__all__'
        extra_fields = ['user_data', 'tipuspagament_data', 'detalls_data']



class PagamentEntradaSerializer(serializers.ModelSerializer):
    user_data = UserSerializer(source='user', read_only=True)
    tipuspagament_data = TipusPagamentSerializer(source='tipuspagament', read_only=True)

    class Meta:
        model = Pagament
        fields = '__all__'
        extra_fields = ['user_data', 'tipuspagament_data']

class EntradaSerializer(serializers.ModelSerializer):
    pagament_data = PagamentEntradaSerializer(source='pagament', read_only=True)
    esdeveniment_data = EsdevenimentSerializer(source='esdeveniment', read_only=True)
    class Meta:
        model = Entrada
        fields = '__all__'
        extra_fields = ['pagament_data','esdeveniment_data']

class EstatEnviamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstatEnviament
        fields = '__all__'
class EnviamentSerializer(serializers.ModelSerializer):
    pagament_data = PagamentSerializer(source='pagament', read_only=True)
    estatenviament_data = EstatEnviamentSerializer(source='estatenviament', read_only=True)

    class Meta:
        model = Enviament
        fields = '__all__'

