from django.contrib import admin

from nani.admin import TranslatableAdmin, TranslatableTabularInline

from web.instances.models import *

from web.accounts.models import UserProfileVariantsForInstance

class UserProfileVariantsForInstanceInline(admin.StackedInline):
    model = UserProfileVariantsForInstance

class CityAdmin(admin.ModelAdmin):
    list_display = ('name','domain',)
    ordering = ('name',)
    search_fields = ('name', 'domain')

class InstanceAdmin(TranslatableAdmin):
    list_display = ('title', 'start_date',)
    filter_horizontal = ('affiliations',)
    inlines = [
        UserProfileVariantsForInstanceInline,
    ]
class NotificationRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'instance')

class PointsAssignmentAdmin(admin.ModelAdmin):
    list_display = ('action', 'points', 'instance')

# Register to admin sites
admin.site.register(Instance, InstanceAdmin)
admin.site.register(Language)
#admin.site.register(Affiliation, AffiliationAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(NotificationRequest, NotificationRequestAdmin)
#admin.site.register(PointsAssignmentAction)
admin.site.register(PointsAssignment, PointsAssignmentAdmin)
