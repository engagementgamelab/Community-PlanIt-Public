import csv
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

def export_emails_for_instance_csv(modeladmin, request, queryset):
    """
    Generic csv export admin action.
    """
    if not request.user.is_staff:
        raise PermissionDenied
    opts = modeladmin.model._meta
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')
    writer = csv.writer(response)
    #field_names = [field.name for field in opts.fields]
    field_names = ['user_profile_email',]
    # Write a first row with header information
    #writer.writerow(field_names)
    # Write data rows
    for obj in queryset.filter(user_profile__user__is_active=True):
        writer.writerow([getattr(obj, field) for field in field_names])
    return response
export_emails_for_instance_csv.short_description = "Export selected profile emails as csv file"
