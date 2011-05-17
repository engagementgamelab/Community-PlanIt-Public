from django.db import models
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from web.games.models import Game
from web.prompts.basic.models import BasicPrompt
from web.responses.map.models import MapResponse

from gmapsfield.fields import GoogleMapsField

# Mapit
class Mapit(Game):
    prompt = models.ForeignKey(BasicPrompt, null=True, blank=True)
    response = models.ForeignKey(MapResponse, null=True, blank=True)

#    object_id = models.PositiveIntegerField()
#    content_type = models.ForeignKey(ContentType)
#    content_object = generic.GenericForeignKey('content_type', 'object_id')

    # Set game type
    def save(self):
        self.game_type = "mapit"
        super(Mapit, self).save()

    class Meta:
        app_label = "games"
        verbose_name = "MapIt Game"
        verbose_name_plural = "MapIt Games"

    def __unicode__(self):
        return "Mapit"

#class BasicPromptInline(admin.TabularInline):
#    model = BasicPrompt
#    extra = 1
#    max_num = 1
#
#class MapResponseInline(admin.TabularInline):
#    model = MapResponse
#    extra = 1
#    max_num = 1
#
#    obj = None
#    def get_formset(self, request, obj=None, **kwargs):
#        self.obj = obj 
#
#        return super(MapResponseInline, self).get_formset(request, obj, **kwargs)
#
#    def formfield_for_manytomany(self, db_field, request, **kwargs):
#        if db_field.name == 'attachment' and getattr(self, 'obj', None):
#            kwargs['queryset'] = Mapit.objects.get(id=self.obj.id).response.attachment.all()
#        elif db_field.name == 'attachment':
#            kwargs['queryset'] = Mapit.objects.filter(id=-2)
#
#        if db_field.name == 'comments' and getattr(self, 'obj', None):
#            kwargs['queryset'] = Mapit.objects.get(id=self.obj.id).response.comments.all()
#        elif db_field.name == 'comments':
#            kwargs['queryset'] = Mapit.objects.filter(id=-2)
#
#        return super(MapResponseInline, self).formfield_for_manytomany(db_field, request, **kwargs)

class MapitAdmin(admin.ModelAdmin):
    list_display = ('title', 'prompt', 'response',)

    exclude = ('instance')

    def save_model(self, request, obj, form, change):
        obj.instance = request.session.get('admin_instance')

        obj.save()

    #inlines = [
    #    BasicPromptInline,
    #    MapResponseInline,
    #]

    exclude = ('prompt','response',)

#    def queryset(self, request):
#        qs = super(MapitAdmin, self).queryset(request)
#        return qs.filter(mission=request.session.get('mission'))

#def mapit_post_save(instance, created, **kwargs):
#    if created:
#        try:
#            g = Game()
#        except:
#            UserProfile.objects.create(user=instance)
#            try:
#                instance.groups.add(Group.objects.get(name='Player'))
#            except Group.DoesNotExist:
#                group = Group(name='Player')
#                group.save()
#                instance.groups.add(group)
#
#models.signals.post_save.connect(mapit_post_save, sender=Mapit)
