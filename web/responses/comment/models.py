import datetime

from django.db import models

from django.contrib import admin

from web.responses.models import Response

class CommentResponse(Response):
    message = models.CharField(default=' ', max_length=1000)
    posted_date = models.DateTimeField(default=datetime.datetime.now, blank='')

    def save(self):
        self.response_type = 'comment'
        super(CommentResponse, self).save()

    class Meta:
        app_label = 'responses'
        verbose_name = 'Comment Response'
        verbose_name_plural = 'Comments Responses'

    def __unicode__(self):
        return 'Comments Response'

class CommentResponseAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(CommentResponseAdmin, self).queryset(request)

        return qs.filter(answer=False)
