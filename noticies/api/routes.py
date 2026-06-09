from rest_framework.routers import DefaultRouter

from noticies.api.views import noticiesApiViewSet

router_noticies = DefaultRouter()

router_noticies.register(
    prefix='noticies', basename='noticies', viewset=noticiesApiViewSet
)