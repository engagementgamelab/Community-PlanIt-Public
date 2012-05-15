from django.contrib import admin
from nani.admin import TranslatableAdmin
from .models import Badge, BadgePerPlayer

class BadgeAdmin(TranslatableAdmin):
    list_display = ('title',)
    ordering = ('title',)
admin.site.register(Badge, BadgeAdmin)


class BadgePerPlayerAdmin(admin.ModelAdmin):
    list_display = ('badge', 'player_screen_name', 'level')
    list_filter = ('badge', )
admin.site.register(BadgePerPlayer, BadgePerPlayerAdmin)
