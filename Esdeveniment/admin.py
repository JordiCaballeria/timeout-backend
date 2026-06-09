from django.contrib import admin
from django.contrib.admin import ModelAdmin
from Esdeveniment.models import *

# Register your models here.
class TipusEsdevenimentAdmin(ModelAdmin):
    pass
admin.site.register(TipusEsdeveniment,ModelAdmin)

class EsdevenimentAdmin(ModelAdmin):
    pass
admin.site.register(Esdeveniment,ModelAdmin)