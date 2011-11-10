from django.contrib import admin

from nani.admin import TranslatableAdmin

from values.models import Value

class ValueAdmin(TranslatableAdmin):
    list_display = ('__str__', 'instance')

admin.site.register(Value, ValueAdmin)
