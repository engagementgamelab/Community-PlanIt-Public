from web.prompts.models import Prompt
from django.db import models
from django.contrib import admin

def determine_path(instance, filename):
    return 'uploads/avatars/'+ filename

class ProfilePrompt(Prompt):
    bio = models.TextField(blank=True, null=True)

    avatar = models.ImageField(upload_to=determine_path)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=64, blank=True, null=True)
    race = models.CharField(max_length=125, blank=True, null=True)

    def save(self):
        self.prompt_type = "profile"
        super(ProfilePrompt, self).save()

    class Meta:
        app_label = "prompts"
        verbose_name = "Profile Prompt"
        verbose_name_plural = "Profile Prompts"

    def render(self):
        return self.bio

    def __unicode__(self):
        return self.bio[:25]

class ProfilePromptAdmin(admin.ModelAdmin):
    exclude = ('download',)
