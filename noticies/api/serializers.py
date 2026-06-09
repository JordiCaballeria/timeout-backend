from rest_framework.serializers import ModelSerializer

from noticies.models import noticies
from Esdeveniment.api.serializers import EsdevenimentSerializer

class NoticiesSerializer(ModelSerializer):
    esdeveniment_data = EsdevenimentSerializer(source='esdeveniment', read_only=True)
    class Meta:
        model = noticies
        fields = ['id', 'titol', 'subtitol', 'path_imatge', 'contingut', 'esdeveniment', 'autor','fotograf','activa','nomes_jugadors','esdeveniment_data', 'data_publicacio']
        extra_kwargs = {'path_imatge': {'required': False}}