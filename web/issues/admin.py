from django.contrib import admin

from web.issues.models import *

admin.site.register(Issue, IssueAdmin)
