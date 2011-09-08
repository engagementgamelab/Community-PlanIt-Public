from django.contrib import admin
from nani.admin import TranslatableAdmin, TranslatableTabularInline
from web.instances.models import Instance, Language, Stake


class StakeInline(TranslatableTabularInline):
    model = Stake
    extra = 1

class InstanceAdmin(TranslatableAdmin):
    list_display = ('title', 'start_date',)
    inlines = [StakeInline]


# Register to admin sites
admin.site.register(Instance, InstanceAdmin)
admin.site.register(Language)
admin.site.register(Stake)
