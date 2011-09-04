import datetime

from nani.admin import TranslatableAdmin
from nani.models import TranslatableModel, TranslatedFields

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from web.accounts.models import determine_path
from web.attachments.models import Attachment
from web.missions.models import Mission

__all__ = ( 'PlayerActivityType','PlayerActivity', 'PlayerMapActivity', 'PlayerEmpathyActivity', 'MultiChoiceActivity', )

def determine_path(instance, filename):
    return 'uploads/'+ str(instance.creationUser.id) +'/'+ filename

class PlayerActivityType(models.Model):
    type = models.CharField(max_length=255)
    displayType = models.CharField(max_length=255)
    defaultPoints = models.IntegerField(default=10)

    def __unicode__(self):
        return self.type

class PlayerActivityBase(TranslatableModel):

    slug = models.SlugField(editable=False)
    creationUser = models.ForeignKey(User)
    mission = models.ForeignKey(Mission, related_name='%(app_label)s_%(class)s_related')
    type = models.ForeignKey(PlayerActivityType)
    createDate = models.DateTimeField(editable=False)
    points = models.IntegerField(blank=True, null=True, default=None)
    attachment = models.ManyToManyField(Attachment, blank=True, null=True)

    class Meta:
        abstract = True

class PlayerActivity(PlayerActivityBase):

    translations = TranslatedFields(
        name = models.CharField(max_length=255),
        question = models.CharField(max_length=1000),
        instructions = models.CharField(max_length=255, null=True, blank=True),
        addInstructions = models.CharField(max_length=255, null=True, blank=True),
        meta = {'ordering': ['name',],
        },
    )

    class Meta:
        verbose_name_plural = 'Player Activities'
        #removing contraint since name is now translated
        #and it seems you cannot mix translated fields
        #unique_together = ('mission', 'type')

    def __unicode__(self):
        return self.safe_translation_getter('name', 'Activity: %s' % self.pk)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.pk)
        self.createDate = datetime.datetime.now()
        super(PlayerActivity, self).save(*args, **kwargs)

    def getPoints(self):
        if self.points == None:
            return self.type.defaultPoints
        else:
            return self.points

class PlayerMapActivity(PlayerActivityBase):
    maxNumMarkers = models.IntegerField(default=5)
    #django-nani complains that no translated fields exist on a sublclass of TraslatableModel
    translations = TranslatedFields(
        tbd = models.CharField(max_length=10),
    )

    translations = TranslatedFields(
        name = models.CharField(max_length=255),
        question = models.CharField(max_length=1000),
        instructions = models.CharField(max_length=255, null=True, blank=True),
        addInstructions = models.CharField(max_length=255, null=True, blank=True),
        meta = {'ordering': ['name',],
        },
    )
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.pk)
        self.createDate = datetime.datetime.now()
        self.type = PlayerActivityType.objects.get(type="map")
        super(PlayerMapActivity, self).save(*args, **kwargs)

class PlayerEmpathyActivity(PlayerActivityBase):
    avatar = models.ImageField(upload_to=determine_path, null=True, blank=True)
    translations = TranslatedFields(
        bio = models.CharField(max_length=1000),
    )
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.createDate = datetime.datetime.now()
        self.type = PlayerActivityType.objects.get(type="empathy")
        super(PlayerEmpathyActivity, self).save(*args, **kwargs)

class MultiChoiceActivity(TranslatableModel):
    activity = models.ForeignKey(PlayerActivity)

    translations = TranslatedFields(
        value = models.CharField(max_length=255),
    )

#***************************************
#admin
class PlayerActivityTypeAdmin(TranslatableAdmin):
    list_display = ('type', 'defaultPoints',)

class PlayerActivityAdmin(TranslatableAdmin):
    list_display = ('pk',) #excluding translated fields 'name', 'question', 
    #'creationUser', 
    #'mission', 'type', 'createDate', 'points'

class PlayerEmpathyActivityAdmin(TranslatableAdmin):
    list_display = ('pk',) #excluding translated fields 'name', 'question', 
    
