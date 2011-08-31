from django.contrib import admin

from web.values.models import *

admin.site.register(Value, ValueAdmin)
