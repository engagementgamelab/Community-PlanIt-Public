from web.instances.models import *

from django.contrib import admin

# Register to admin sites
admin.site.register(Instance, InstanceAdmin)
admin.site.register(PointsAssignment, PointsAssignmentAdmin)
