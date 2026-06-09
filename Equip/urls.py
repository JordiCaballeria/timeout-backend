from django.urls import path

from Equip.views import *
from Equip.api.views import *

app_name = 'multipleurl'
urlpatterns = [
    path('equips/', EquipsApiView.as_view(), name="equips"),
    path('divisions/', DivisioApiView.as_view(), name="divisions"),
    path('categories/', CategoriaApiView.as_view(), name="categories"),
    path('esports/', EsportApiView.as_view(), name="esports"),
]

