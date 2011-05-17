from django.contrib import admin
from django.db import models
from web.responses.models import Response

class Choice(models.Model):
    text = models.CharField(max_length=260)

    class Meta:
        app_label = 'responses'

    def __unicode__(self):
        return self.text

class ChoicesResponse(Response):
    choices = models.ManyToManyField(Choice)

    def save(self):
        self.response_type = 'choices'
        super(ChoicesResponse, self).save()

    class Meta:
        app_label = 'responses'
        verbose_name = 'Multiple Choice Response'
        verbose_name_plural = 'Multiple Choice Responses'

    def __unicode__(self):
        return 'Multiple Choice Response'

class ChoicesResponseAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(ChoicesResponseAdmin, self).queryset(request)

        return qs.filter(answer=False)
