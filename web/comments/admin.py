from web.comments.models import *
from django.contrib import admin

admin.site.register(Comment, CommentAdmin)
