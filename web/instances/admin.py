from django.contrib import admin
from nani.admin import TranslatableAdmin
from web.instances.models import Instance, Language


class InstanceAdmin(TranslatableAdmin):
    list_display = ('start_date',) #could not be used with nani:, 'name', 


# Register to admin sites
admin.site.register(Instance, InstanceAdmin)
admin.site.register(Language)
