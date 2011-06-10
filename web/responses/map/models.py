from django.db import models
from django.contrib import admin

from gmapsfield.fields import GoogleMapsField
from web.responses.models import Response

class MapResponse(Response):
    map = GoogleMapsField()
    type = models.CharField(max_length=260, choices=(('Shape','Shape'), ('Line','Line'), ('Point','Point')), default='Point')
    message = models.CharField(default=' ', max_length=1000)

    game = models.ForeignKey('games.Game', related_name='mapresponse_game', null=True, blank=True)
    
    def save(self):
        self.response_type = 'map'
        super(MapResponse, self).save()

    class Meta:
        app_label = 'responses'
        verbose_name = 'Map Response'
        verbose_name_plural = 'Map Responses'

    def __unicode__(self):
        label = 'Location: '+ str(self.map.coordinates)
        return label[:25]

class MapResponseAdmin(admin.ModelAdmin):
    exclude = ('game','comments','attachment','flagged')
