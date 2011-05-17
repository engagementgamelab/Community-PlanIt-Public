from django.contrib import admin

from web.responses.map.models import *
from web.responses.choices.models import *
from web.responses.comment.models import *

admin.site.register(MapResponse, MapResponseAdmin)
admin.site.register(CommentResponse)
admin.site.register(Choice)
admin.site.register(ChoicesResponse)
