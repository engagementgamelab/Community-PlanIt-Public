from django.contrib import admin
from .models import Award, PlayerAward

class AwardsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ('title',)
admin.site.register(Award, AwardsAdmin)


class PlayerAwardAdmin(admin.ModelAdmin):
    list_display = ('award', 'level')
    list_filter = ('award', )
admin.site.register(PlayerAward, PlayerAwardAdmin)
