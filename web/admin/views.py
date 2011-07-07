
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseRedirect, Http404


def index(request):
    return HttpResponse("HERE")