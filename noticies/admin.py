from django.contrib import admin

from noticies.models import noticies

@admin.register(noticies)
class NoticiesAdmin(admin.ModelAdmin):
    pass
