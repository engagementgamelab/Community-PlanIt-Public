from django.contrib import admin

from nani.admin import TranslatableAdmin, TranslatableTabularInline

from web.instances.models import Instance, Language, Stake

class InstanceAdmin(TranslatableAdmin):
    list_display = ('title', 'start_date',)

class StakeAdmin(TranslatableAdmin):
    list_display = ('__str__', 'instance',)

# Register to admin sites
admin.site.register(Instance, InstanceAdmin)
admin.site.register(Language)
admin.site.register(Stake, StakeAdmin)
