from crowds.models import *
from django.contrib import admin

class CrowdAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'creator', 'instance')
    list_filter = ('instance', 'start_date')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'attachments' and getattr(self, 'obj', None):
            kwargs['queryset'] = Crowd.objects.get(id=self.obj.id).attachments.all()
        elif db_field.name == 'attachments':
            kwargs['queryset'] = Crowd.objects.filter(id=-2)

        if db_field.name == 'comments' and getattr(self, 'obj', None):
            kwargs['queryset'] = Crowd.objects.get(id=self.obj.id).comments.all()
        elif db_field.name == 'comments':
            kwargs['queryset'] = Crowd.objects.filter(id=-2)
        return super(CrowdAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        self.obj = obj 
        return super(CrowdAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(Crowd, CrowdAdmin)
#admin.site.register(PlayerChallenge)
