import datetime
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib import admin
from django.contrib.contenttypes import generic

from web.instances.models import InstanceView
from web.games.models import Game
from web.games.mapit.models import Mapit
from web.games.thinkfast.models import ThinkFast
from web.games.othershoes.models import OtherShoes

class QuerySetManager(models.Manager):
    def get_query_set(self):
        return self.model.QuerySet(self.model)

#TODO: Set up a generic foreign key from game to mission, get rid of generic.GenericRelation
#There is no need for that here.
#Why does the description field exist if it can be null?
class Mission(models.Model):
    topic = models.CharField(max_length=45)
    slug = models.SlugField(editable=False)
    start_date = models.DateField()
    end_date = models.DateField()

    video = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    instance = models.ForeignKey(InstanceView, editable=False)
    #games = generic.GenericRelation(Game)

    # Faking out the objects collection to pull from the inner model
    # class.
    objects = QuerySetManager()

    class QuerySet(models.query.QuerySet):
        def past(self):
            return self.filter(end_date__lte=datetime.datetime.now()).order_by('start_date')

        def future(self):
            return self.filter(start_date__gt=datetime.datetime.now()).order_by('start_date')

        def current(self):
            return self.filter(start_date__lte=datetime.datetime.now()).filter(end_date__gt=datetime.datetime.now()).order_by('start_date')

    def is_active(self):
        return self.start_date <= datetime.date.today() and self.end_date >= datetime.date.today()

    def is_expired(self):
        return self.start_date < datetime.date.today() and self.end_date < datetime.date.today()

    def is_notstarted(self):
        return self.start_date > datetime.date.today() and self.end_date > datetime.date.today()

    def save(self):
        self.slug = slugify(self.topic)
        super(Mission, self).save()

    def __unicode__(self):
        return self.topic[:25]

class MapitInline(generic.GenericStackedInline):
    model = Mapit
    extra = 1

class ThinkFastInline(generic.GenericStackedInline):
    model = ThinkFast
    extra = 1

class OtherShoesInline(generic.GenericStackedInline):
    model = OtherShoes
    extra = 1

class MissionAdmin(admin.ModelAdmin):
    list_display = ('topic', 'start_date', 'end_date')

    inlines = [
        MapitInline,
        ThinkFastInline,
        OtherShoesInline,
    ]

    def queryset(self, request):
        qs = super(MissionAdmin, self).queryset(request)
        return qs.filter(instance=request.session.get('admin_instance'))

    def save_model(self, request, obj, form, change):
        obj.instance = request.session.get('admin_instance')
        obj.save()

    obj = None
    def get_form(self, request, obj=None, **kwargs):
        self.obj = obj 
        return super(MissionAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'games' and getattr(self, 'obj', None):
            kwargs['queryset'] = Mission.objects.get(id=self.obj.id).games.all()
        elif db_field.name == 'games':
            kwargs['queryset'] = Mission.objects.filter(id=-2)
        return super(MissionAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
