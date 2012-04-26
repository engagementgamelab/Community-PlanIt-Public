import os.path

from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import get_language

from nani.models import TranslatableModel, TranslatedFields
from nani.manager import TranslationManager

def determine_path(instance, filename):
    return os.path.join('uploads/cities/', str(instance.domain), filename)


class Badge(TranslatableModel):
    slug = models.SlugField()
    title = models.CharField(max_length=255, verbose_name="Title (non-translatable)")

    translations = TranslatedFields(
        name = models.CharField(max_length="100"),
        description = models.TextField(),
        #meta = {'get_latest_by': 'start_date'}
    )

