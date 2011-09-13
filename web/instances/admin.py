from django.contrib import admin

from nani.admin import TranslatableAdmin, TranslatableTabularInline

from web.instances.models import Instance, Language, NotificationRequest, PointsAssignment, PointsAssignmentAction, Stake

class InstanceAdmin(TranslatableAdmin):
    list_display = ('title', 'start_date',)

class NotificationRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'instance')

class PointsAssignmentAdmin(admin.ModelAdmin):
    list_display = ('action', 'points', 'instance')

class StakeAdmin(TranslatableAdmin):
    list_display = ('__str__', 'instance',)

# Register to admin sites
admin.site.register(Instance, InstanceAdmin)
admin.site.register(Language)
admin.site.register(NotificationRequest, NotificationRequestAdmin)
admin.site.register(PointsAssignmentAction)
admin.site.register(PointsAssignment, PointsAssignmentAdmin)
admin.site.register(Stake, StakeAdmin)
