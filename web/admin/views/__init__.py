from django.shortcuts import render_to_response

def verify(request, template="admin/backend_not_superuser.html"):
    user = request.user
    if user.is_superuser:
        return None
    else:
        return render_to_response(template, RequestContext(request, context))
