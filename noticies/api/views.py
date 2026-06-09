from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from noticies.models import noticies
from noticies.api.serializers import NoticiesSerializer
from django_filters.rest_framework import DjangoFilterBackend
class noticiesApiViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = NoticiesSerializer
    queryset = noticies.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['activa','esdeveniment','nomes_jugadors']

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)