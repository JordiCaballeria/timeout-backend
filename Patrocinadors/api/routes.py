from rest_framework.routers import DefaultRouter

from Patrocinadors.api.views import patorcinadorsApiViewSet

router_patrocinadors = DefaultRouter()

router_patrocinadors.register(
    prefix='patrocinadors', basename='patrocinadors', viewset=patorcinadorsApiViewSet
)