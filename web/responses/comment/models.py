from django.contrib import admin
from django.db import models
from web.responses.models import Response

class CommentResponse(Response):
    message = models.CharField(default=' ', max_length=260)
    posted_date = models.DateTimeField(auto_now_add=True, blank='')

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
