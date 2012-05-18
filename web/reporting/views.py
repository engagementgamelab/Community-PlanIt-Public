from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

#@login_required
def run_report(request, report_name, instance_id):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("admin:index"))

    print "running %s report for game %s" % (report_name, instance_id)
    from uwsgiutils.tasks import uwsgi_run_report
    kwargs = dict(
        report_name=str(report_name), 
        instance_id=str(instance_id),
    )
    uwsgi_run_report.spool(**kwargs)
    return HttpResponseRedirect(reverse("admin:index"))

    """
    try:
        # uwsgi spool
        from uwsgiutils.tasks import uwsgi_run_demographic_report
        uwsgi_run_demographic_report.spool()
    except ImportError:
        # it is not possible to import uwsgi
        # from certain environments such as from pyshell
        # ignoring the ImportError
        pass
    return HttpResponseRedirect(reverse("admin:index"))
    """
