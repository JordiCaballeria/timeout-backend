from rest_framework.serializers import ModelSerializer
from Patrocinadors.models import *

class PatrocinadorsSerializer(ModelSerializer):
    class Meta:
        model = Patrocinador
        fields = '__all__'
        extra_kwargs = {'path_imatge': {'required': False}}
