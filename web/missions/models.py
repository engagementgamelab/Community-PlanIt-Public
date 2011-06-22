import datetime
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib import admin
from web.instances.models import Instance

class QuerySetManager(models.Manager):
    def get_query_set(self):
        return self.model.QuerySet(self.model)

#TODO: Set up a generic foreign key from game to mission, get rid of generic.GenericRelation
#There is no need for that here.
#Why does the description field exist if it can be null?
class Mission(models.Model):
    name = models.CharField(max_length=45)
    slug = models.SlugField(editable=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    video = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    instance = models.ForeignKey(Instance, editable=False)
    
    def is_active(self):
        if datetime.datetime.now() >= self.start_date and datetime.datetime.now() <= self.end_date:
            return True;
        else:
            return False;
        
    def is_expired(self):
        if datetime.datetime.now() >= self.end_date:
            return True
        else:
            return False
    
    def is_started(self):
        if datetime.datetime.now() >= self.start_date:
            return True
        else:
            return False
    
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

    def save(self):
        self.slug = slugify(self.topic)
        super(Mission, self).save()

    def __unicode__(self):
        return self.topic[:25]

class MissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')

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
