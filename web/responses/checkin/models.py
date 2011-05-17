from django.db import models

from gmapsfield.fields import GoogleMapsField

from web.responses.models import Response

class CheckinResponse(Response):
    location = GoogleMapsField()
    
    def save(self):
        self.response_type = "checkin"
        super(CheckinResponse, self).save()

    class Meta:
        app_label = "responses"
        verbose_name = "Check-in Response"
        verbose_name_plural = "Check-in Responses"
