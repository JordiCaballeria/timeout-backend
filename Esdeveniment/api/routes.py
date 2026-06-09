from rest_framework.routers import DefaultRouter

from Esdeveniment.api.views import EsdevenimentApiViewSet, TipusEsdevenimentApiViewSet

router_esdeveniments = DefaultRouter()

router_esdeveniments.register(
    prefix='esdeveniments', basename='esdeveniments', viewset=EsdevenimentApiViewSet
)

router_tipusesdeveniments = DefaultRouter()

router_tipusesdeveniments.register(
    prefix='tipusesdeveniments', basename='tipusesdeveniments', viewset=TipusEsdevenimentApiViewSet
)