from django.urls import path
from rest_framework.routers import DefaultRouter
from User.api.views import UserApiViewSet, UserView, RolApiViewSet, RolUsuariApiViewSet, PermisosApiViewSet, \
    CustomTokenObtainPairView
from django.urls import path

router_user = DefaultRouter()
router_rol = DefaultRouter()
router_rolusuari = DefaultRouter()
router_permisos = DefaultRouter()
router_user.register(
    prefix='users',
    basename='users',
    viewset=UserApiViewSet,
)

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('auth/me/', UserView.as_view()),
]


router_rol.register(
    prefix='rol',
    basename='rol',
    viewset=RolApiViewSet,
)

router_rolusuari.register(
    prefix='rolusuari',
    basename='rolusuari',
    viewset=RolUsuariApiViewSet,
)

router_permisos.register(
    prefix='permisos',
    basename='permisos',
    viewset=PermisosApiViewSet,
)