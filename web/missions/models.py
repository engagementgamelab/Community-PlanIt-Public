import datetime
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib import admin
from web.instances.models import Instance

class MissionQueryMixin(object):
    def past(self):
        return self.filter(end_date__lt=datetime.datetime.now()).order_by('-end_date')

    def future(self):
        return self.filter(start_date__gt=datetime.datetime.now()).order_by('start_date')

    def active(self):
        now = datetime.datetime.now()
        return self.filter(start_date__lte=now, end_date__gte=now).order_by('start_date')

class MissionQuerySet(models.query.QuerySet, MissionQueryMixin):
    pass

class MissionManager(models.Manager, MissionQueryMixin):
    def get_query_set(self):
        return MissionQuerySet(self.model, using=self._db)

class Mission(models.Model):
    instance = models.ForeignKey(Instance, related_name='missions')
    name = models.CharField(max_length=45)
    slug = models.SlugField(editable=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(blank=True)
    video = models.TextField(blank=True)
    
    objects = MissionManager()

    class Meta:
        get_latest_by = 'start_date'
        
    def is_active(self):
        now = datetime.datetime.now()
        return self.start_date <= now and now <= self.end_date
        
    def is_expired(self):
        return datetime.datetime.now() > self.end_date
    
    def is_started(self):
        return datetime.datetime.now() >= self.start_date
    
    def save(self):
        self.slug = slugify(self.name)
        super(Mission, self).save()

    def __unicode__(self):
        return self.name

class MissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'instance')

    def queryset(self, request):
        qs = super(MissionAdmin, self).queryset(request)
        return qs.filter(instance=request.session.get('admin_instance'))

    def save_model(self, request, obj, form, change):
        #obj.instance = request.session.get('admin_instance')
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
