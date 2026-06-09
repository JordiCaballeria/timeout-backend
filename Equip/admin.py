from django.contrib import admin
from django.contrib.admin import ModelAdmin
from Equip.models import *

class CategoriaAdmin(ModelAdmin):
    pass
admin.site.register(Categoria,ModelAdmin)

class DivisioAdmin(ModelAdmin):
    pass
admin.site.register(Divisio,ModelAdmin)

class EsportAdmin(ModelAdmin):
    pass
admin.site.register(Esport,ModelAdmin)

class EquipAdmin(ModelAdmin):
    pass
admin.site.register(Equip,ModelAdmin)

class EquipUsuarisAdmin(ModelAdmin):
    pass
admin.site.register(EquipUsuaris,ModelAdmin)



