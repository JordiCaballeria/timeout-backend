from django.contrib import admin
from django.contrib.admin import ModelAdmin
from Botiga.models import *


class ProducteAdmin(ModelAdmin):
    pass
admin.site.register(Producte,ModelAdmin)

class EntradaAdmin(ModelAdmin):
    pass
admin.site.register(Entrada,ModelAdmin)

class TipusProductesAdmin(ModelAdmin):
    pass
admin.site.register(TipusProducte,ModelAdmin)

class TallesAdmin(ModelAdmin):
    pass
admin.site.register(Talles,ModelAdmin)

class ProducteTallesAdmin(ModelAdmin):
    pass
admin.site.register(ProducteTalles,ModelAdmin)

class PagamentAdmin(ModelAdmin):
    pass
admin.site.register(Pagament,ModelAdmin)

class DetallsPagamentAdmin(ModelAdmin):
    pass
admin.site.register(DetallsPagament,ModelAdmin)

class ImatgesProducteAdmin(ModelAdmin):
    pass
admin.site.register(ImatgesProducte,ModelAdmin)
