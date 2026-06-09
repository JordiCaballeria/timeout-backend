from rest_framework.routers import DefaultRouter
from Equip.api.views import EquipApiViewSet, EquipsApiView, DivisioApiView, DivisioApiViewSet, CategoriaApiView, \
    CategoriaApiViewSet, EsportApiViewSet, EsportApiView
from django.urls import path

router_equips = DefaultRouter()
router_divisions = DefaultRouter()
router_categories = DefaultRouter()
router_esports = DefaultRouter()

router_equips.register(
    prefix='equips',
    basename='equips',
    viewset=EquipApiViewSet,
)

router_divisions.register(
    prefix='divisions',
    basename='divisions',
    viewset=DivisioApiViewSet,
)

router_categories.register(
    prefix='categories',
    basename='categories',
    viewset=CategoriaApiViewSet,
)

router_esports.register(
    prefix='esports',
    basename='esports',
    viewset=EsportApiViewSet,
)

urlpatterns = [
    path('equips/', EquipsApiView.as_view()),
    path('divisions/', DivisioApiView.as_view()),
    path('categories/', CategoriaApiView.as_view()),
    path('esports/', EsportApiView.as_view()),
]
