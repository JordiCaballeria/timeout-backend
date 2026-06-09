from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import *
from User.models import *


class RolAdmin(ModelAdmin):
    pass
admin.site.register(Rol,ModelAdmin)

class PermisosAdmin(ModelAdmin):
    pass
admin.site.register(Permisos,ModelAdmin)

class RolUsuariAdmin(ModelAdmin):
    pass
admin.site.register(RolUsuari,ModelAdmin)

class UserAdmin(ModelAdmin):
    pass
admin.site.register(User,ModelAdmin)