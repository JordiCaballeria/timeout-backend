from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from Equip.views import update_jugadors, update_entrenadors, equip_client_id
from Esdeveniment.views import esdeveniment_partit, equipsclient, esdeveniments_avui
from Patrocinadors.api.routes import router_patrocinadors
from User.api.routes import router_user, router_rol, router_rolusuari, router_permisos
from Equip.api.routes import router_equips, router_categories, router_esports, router_divisions
from User.api.views import RegistrationView, ActivateUserView, UserPhotoUpdateAPIView, JugadoresView
from User.views import actualizar_roles, entrenadores, enviar_email, password_reset_request,\
    pagament_stripe, nou_soci, resum, enviar_contacte
from noticies.api.routes import router_noticies
from Esdeveniment.api.routes import router_esdeveniments, router_tipusesdeveniments
from Botiga.api.routes import router_talles, router_pagaments, router_productes, router_entrades, \
    router_productes_talles, router_detalls_pagament, router_tipus_producte, router_imatges_producte, router_enviaments, \
    router_tipuspagament, router_estatenviaments
from Botiga.views import crear_producte, crear_imatges_producte, actualitzar_producte, crear_pagament, vendre_entrades, \
    validar_entrada
from corsheaders.middleware import CorsMiddleware
from django.middleware.common import CommonMiddleware
from django.contrib.auth import views as auth_views
from django.http import JsonResponse

def health(request):
    return JsonResponse({'status': 'ok'})

admin.autodiscover()

# Agregar el middleware de CorsMiddleware y CommonMiddleware para que se aplique a todas las solicitudes.
middleware = [
    CorsMiddleware,
    CommonMiddleware,
]

schema_view = get_schema_view(
   openapi.Info(
      title="TimeOut API doc",
      default_version='v1',
      description="Documentació de la API de Timeout",
      terms_of_service="https://www.timeout.com",
      contact=openapi.Contact(email="igonzalezm2@ies-sabadell.cat"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

from Equip.api.views import *

urlpatterns = [
    path('health/', health, name='health'),
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/', include(router_user.urls)),
    path('api/', include(router_rol.urls)),
    path('api/', include(router_rolusuari.urls)),
    path('api/', include(router_equips.urls)),
    path('api/', include(router_esports.urls)),
    path('api/', include(router_divisions.urls)),
    path('api/', include(router_categories.urls)),
    path('api/', include(router_noticies.urls)),
    path('api/', include(router_esdeveniments.urls)),
    path('api/', include(router_tipusesdeveniments.urls)),
    path('api/', include(router_permisos.urls)),
    path('api/', include(router_talles.urls)),
    path('api/', include(router_tipus_producte.urls)),
    path('api/', include(router_productes.urls)),
    path('api/', include(router_productes_talles.urls)),
    path('api/', include(router_pagaments.urls)),
    path('api/', include(router_entrades.urls)),
    path('api/', include(router_detalls_pagament.urls)),
    path('api/', include(router_imatges_producte.urls)),
    path('api/', include(router_patrocinadors.urls)),
    path('api/', include(router_enviaments.urls)),
    path('api/', include(router_tipuspagament.urls)),
    path('api/', include(router_estatenviaments.urls)),
    path('api/', include('User.api.routes')),
    path('api/', include('Equip.api.routes')),
    path('api/updaterols/', actualizar_roles, name='update-roles'),
    path('api/updateequipjugadors/', update_jugadors, name='update-equips-jugadors'),
    path('api/updateequipentrenadors/', update_entrenadors, name='update-equips-entrenadors'),
    path('api/crear_pagament/', crear_pagament, name='crear-pagament'),
    path('api/vendre_entrades/', vendre_entrades, name='vendre-entrades'),
    path('api/jugadores/', JugadoresView.as_view(), name='jugadores'),
    path('api/entrenadores/', entrenadores, name='entrenadores'),
    path('api/enviar-email/', enviar_email, name='enviar_email'),
    path('api/register/', RegistrationView.as_view(), name='register'),
    path('api/activate/<int:pk>/<str:token>/', ActivateUserView.as_view(), name='activate-user'),
    path('api/imageusers/<int:pk>/photo/', UserPhotoUpdateAPIView.as_view(), name='user-photo-update'),
    path('api/partits/', esdeveniment_partit, name='esdeveniment-partit'),
    path('api/crear_producte/', crear_producte, name='crear_producte'),
    path('api/actualitzar_producte/', actualitzar_producte, name='actualitzar_producte'),
    path('api/insertar_imatges/', crear_imatges_producte, name='insertar_imatges'),
    path('api/pagament_stripe/', pagament_stripe, name='pagament-stripe'),
    path('api/nou_soci/', nou_soci, name='nou-soci'),
    path('api/resum/', resum, name='resum'),
    path('api/equipsclient/<int:equip_id>/', equip_client_id, name='equip_client_id'),
    path('api/equipsclient/', equipsclient, name='equipsclient'),
    path('api/enviar_contacte/', enviar_contacte, name='enviar_contacte'),
    path('api/validar_entrada/', validar_entrada, name='validar_entrada'),
    path('api/esdeveniments_avui/', esdeveniments_avui, name='esdeveniments_avui'),
    # Ruta para la vista de recuperació de password
    path('api/password_reset/', password_reset_request, name='password_reset'),

    # Ruta per a la vista de confirmació de restablecimient de password
    path('api/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),

    # Ruta para la vista d'èxit en restablecimient de password
    path('api/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),

]

urlpatterns += [
    re_path(r'^uploads/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]