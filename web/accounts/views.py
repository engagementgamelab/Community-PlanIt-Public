import urlparse
import datetime
import math
import re

from localeurl.models import reverse
from localeurl.utils import strip_path, locale_path

from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, RequestContext, loader
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext as _, get_language
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect


from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import get_current_site

from web.accounts.forms import *
from web.accounts.models import Notification, UserProfile
from web.answers.models import Answer
from web.challenges.models import Challenge, PlayerChallenge
from web.comments.forms import CommentForm
from web.instances.models import Instance
from web.missions.models import Mission
from web.player_activities.models import PlayerActivity
from web.reports.actions import ActivityLogger, PointsAssigner
from web.reports.models import Activity
from web.values.models import *
from web.core.utils import _fake_latest

from PIL import Image

@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            netloc = urlparse.urlparse(redirect_to)[1]

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            user = form.get_user()
            up = user.get_profile()
            lang = up.preferred_language

            if lang in dict(settings.LANGUAGES).keys():
            	spath = strip_path(redirect_to)[1]
                return HttpResponseRedirect(locale_path(spath, lang))

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    context.update(extra_context or {})
    return render_to_response(template_name, 
                              context,
                              context_instance=RequestContext(
                                    request, current_app=current_app
                              )
    )



# This function is used for registration and forgot password as they are very similar.
# It will take a form and determine if the email address is valid and then generate
# a temporary random password.
def validate_and_generate(base_form, request, callback):
    form = base_form( )
    if request.method == 'POST':
        form = base_form(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = None
            firstName = None
            lastName = None
            if form.cleaned_data.has_key("password"):
                password = form.cleaned_data['password']
            else:
                password = User.objects.make_random_password(length=10)
            if request.POST.get('firstName', None) != None:
                firstName = form.cleaned_data['firstName']
            if request.POST.get('lastName', None) != None:
                lastName = form.cleaned_data['lastName']
            return callback(firstName, lastName, email, password, form)
    return form

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user)
    paginator = Paginator(notifications, 5)

    page = request.GET.get('page', 1)
    notifications_page = paginator.page(page)

    data = {
        'paginator': paginator,
        'notifications_page': notifications_page,
    }

    if request.user.get_profile().instance:
        data['instance'] = request.user.get_profile().instance

    for notification in notifications_page.object_list:
        if notification.read == False:
            notification.unread = True
        notification.read = True
        notification.save()

    return render_to_response(
        'accounts/notifications.html',
        data,
        context_instance=RequestContext(request)
    )

def register(request):
    def valid(firstName, lastName, email, password, form):
        player = User.objects.create(email=email,first_name=firstName, last_name=lastName, is_active=True)
        player.set_password(password)
        player.save()
        player = auth.authenticate(username=email, password=password)
        auth.login(request, player)
        player.save()
        uinfo = player.get_profile()
        uinfo.instance = form.cleaned_data['instance']
        uinfo.preferred_language = form.cleaned_data['preferred_language']
        uinfo.coins = 0
        uinfo.points = 0
        uinfo.points_multiplier = 0
        uinfo.accepted_term = False
        uinfo.accepted_research = False
        uinfo.save()
        
        tmpl = loader.get_template('accounts/email/welcome.html')
        context = Context({
            'instance': uinfo.instance,
            'first_name': firstName
        })
        body = tmpl.render(context)
        
        send_mail(_('Welcome to Community PlanIt!'), body, settings.NOREPLY_EMAIL, [email], fail_silently=False)
        messages.success(request, _("Thanks for signing up!"))
        
        return HttpResponseRedirect(reverse('accounts:dashboard'))

    # If not valid, show normal form
    form = validate_and_generate(RegisterForm, request, valid)
    if(isinstance(form, RegisterForm)):
        tmpl = loader.get_template('accounts/register.html')
        return HttpResponse(tmpl.render(RequestContext(request,{
            'form': form,    
        })))
    else:
        return form

# Forgot your password
def forgot(request):
    def valid(firstName, lastName, email, password, form):
        # Send a new password and update account
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        send_mail(_('Password Changed'), _('Your temporary password is: %(password)s') % { 'password': password }, settings.NOREPLY_EMAIL, [email])
        messages.success(request, _('A temporary password has been sent to your email address.'))

        return HttpResponseRedirect(reverse('accounts:login'))
        
    # If not valid, show normal form
    form = validate_and_generate(ForgotForm, request, valid)
    if(isinstance(form, ForgotForm)):
        tmpl = loader.get_template('accounts/forgot.html')
        return HttpResponse(tmpl.render(RequestContext(request, {
            'form': form,
        })))
    else:
        return form

# Edit profile
@login_required
def edit(request):
    try:
        profile = request.user.get_profile()
    except:
        return Http404
    
    change_password_form = ChangePasswordForm()
    profile_form = UserProfileForm(instance=profile, 
                                   initial={'myInstance': profile.instance.id if profile.instance != None else 0,
                                            'education': profile.education.id if profile.education != None else 0,
                                            'income': profile.income.id if profile.income != None else 0,
                                            'living': profile.living.id if profile.living != None else 0,
                                            'gender': profile.gender.id if profile.gender != None else 0,
                                            'race': profile.race.id if profile.race != None else 0,
                                            'stake': profile.stake.id if profile.stake != None else 0,
                                            'first_name': profile.user.first_name if profile.user.first_name != None else "",
                                            'last_name': profile.user.last_name if profile.user.last_name != None else "",
                                            'email': profile.email if profile.email != None else "",
                                            'birth_year': profile.birth_year if profile.birth_year != None else "",
                                            'preferred_language': profile.preferred_language,
                                            
                                            })
    if request.method == 'POST':
        
        #files = ""
        #post = ""
        #for x in request.FILES:
        #    files = "%s%s: %s\n" % (files, x, request.FILES[x])
        #for x in request.POST: 
        #    post = "%s%s: %s\n" % (post, x, request.POST[x])
        #return HttpResponse("FILES: %s \nPOST: %s \n" % (files, post))
        
        # Change password form moved to user profile
        if request.POST['form'] == 'change_password':
            change_password_form = ChangePasswordForm(request.POST)
            if change_password_form.is_valid():
                password = change_password_form.cleaned_data['password']
                confirm = change_password_form.cleaned_data['confirm']
                
                request.user.set_password(confirm)
                request.user.save()
                messages.success(request, "Sucessfully updated password")
        else:
            # User profile form updated, not change password
            profile_form = UserProfileForm(data=request.POST, files=request.FILES, instance=profile)
            if profile_form.is_valid():
                #Changing instances
                if (request.POST.get('myInstance', None) == None or request.POST['myInstance'] == ''): #reset to the None object
                    profile.instance = None
                else:
                    ins = Instance.objects.filter(id=request.POST.get('myInstance'))
                    if (len(ins) > 0):
                        profile.instance = ins[0]
                    else:
                        profile.instance = None

                #changing birth year (needed because of the int)
                #This fails with the birth_year being blank and python can not convert
                #a '' to an int
                if (request.POST.get('birth_year', None) == None or request.POST.get('birth_year', None) == ''):
                    profile.birth_year = None
                else:
                    profile.birth_year = int(profile_form.cleaned_data['birth_year'])

                #updating email address
                #if (request.POST.get('email', None) == None or request.POST.get('email', None) == ''):
                #    profile.user.email = None
                #else:
                #    profile.user.email = profile_form.cleaned_data['email']

                if (request.POST.get('first_name', None) == None or request.POST.get('first_name', None) == ''):
                    profile.user.first_name = None
                else:
                    profile.user.first_name = profile_form.cleaned_data['first_name']

                if (request.POST.get('last_name', None) == None or request.POST.get('last_name', None) == ''):
                    profile.user.last_name = None
                else:
                    profile.user.last_name = profile_form.cleaned_data['last_name']

                profile.user.save()

                if request.FILES.get('avatar', None) != None:
                    profile.avatar = request.FILES['avatar']
                profile.save()
                profile_form.save()

                if not profile.editedProfile:
                    try:
                        # TODO: Break this out into a function
                        if len(profile.affiliations) and profile.accepted_term and profile.accepted_research and len(profile.phone_number):

                            profile.completed = True
                            profile.save()
                            PointsAssigner().assign(request.user, 'profile_completed')
                    except:
                        pass

                return HttpResponseRedirect(reverse('accounts:dashboard'))
            #else: #uncomment this
            #    s = "error: "
            #    for err in profile_form.errors:
            #        s = "%s%s %s\n" % (s, err, profile_form.errors[err])
            #    return HttpResponse(s)

    tmpl = loader.get_template('accounts/profile_edit.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'profile_form': profile_form,
        'change_password_form': change_password_form,
        'user': request.user,
    })))

@login_required
def profile(request, id):
    player = get_object_or_404(User, id=id)
    profile = player.get_profile()
    
    instance = profile.instance
    log = Activity.objects.filter(instance=instance, user=player).order_by('-date')[:6]    
    comment_form = CommentForm(data=request.POST or None)
    
    if request.method == 'POST':        
        if comment_form.is_valid():           
            comment = profile.comments.create(
                content_object=profile,                 
                user=request.user,
                instance=instance,
            ) 
            try:
                locale = request.META['PATH_INFO'].split('/')[1]
            except:
                locale = get_language()
            comment.translate(locale)              
            comment.message = u'%s' % comment_form.cleaned_data['message']
            comment.save()

            if request.user != player:
                message = "%s commented on your profile" % (
                    request.user.get_profile().screen_name
                )
                player.notifications.create(content_object=profile, message=message)

            if request.POST.has_key('yt-url'):
                url = request.POST.get('yt-url')
                if url:
                    comment.attachment.create(
                        file=None,
                        url=url,
                        type='video',
                        user=request.user,
                        instance=instance
                    )            
            if request.FILES.has_key('picture'):
                file = request.FILES.get('picture')
                picture = Image.open(file)
                if (file.name.rfind(".") -1):
                    file.name = "%s.%s" % (file.name, picture.format.lower())
                comment.attachment.create(
                    file=request.FILES.get('picture'),
                    user=request.user,
                    instance=instance
                )           
            return HttpResponseRedirect(reverse('accounts_profile', args=[id]))    
        

    followingme = []

    for p in User.objects.select_related():
        try:
            if player and player.get_profile() and player in p.get_profile().following.all():
                followingme.append(p)
        except:
            pass
    
    values = Value.objects.filter(instance=request.user.get_profile().instance)
    community_spent = values.aggregate(Sum('coins'))['coins__sum'] or 0
    
    value_wrapper = []
    player_values = PlayerValue.objects.filter(user=request.user)
    
    player_spent = player_values.aggregate(Sum('coins'))['coins__sum'] or 0

    for value in values:
        player_value = player_values.filter(value=value)
        coins = float(value.coins)
        if len(player_value) > 0:
            value_wrapper.append({ 'value': value, 'coins': coins, 'player_coins': player_value[0].coins, 
                                  'percent': 0 if community_spent == 0 else (coins/community_spent)*100 })
        else:
            value_wrapper.append({ 'value': value, 'coins': coins, 'player_coins': 0,
                                   'percent': 0 if community_spent == 0 else (coins/community_spent)*100 })    
    
    tmpl = loader.get_template('accounts/profile.html')
    
    return HttpResponse(tmpl.render(RequestContext(request, {
        'player': player,
        'comment_form': comment_form,
        'instance': instance,
        'followingme': followingme,
        'log': log,
        'player_spent': player_spent,
        'value_wrapper': value_wrapper,
    })))

@login_required
def follow(request, id):
    u = User.objects.get(id=id)
    request.user.get_profile().following.add( u )
    ActivityLogger().log(request.user, request, u.get_profile().screen_name, 'started following', '/player/'+ id, 'profile')

    return HttpResponseRedirect('/player/'+ str(id))

@login_required
def unfollow(request, id):
    request.user.get_profile().following.remove( User.objects.get(id=id) )

    return HttpResponseRedirect('/player/'+ str(id))

@login_required
def dashboard(request):
    tmpl = loader.get_template('accounts/dashboard.html')

    instance = None

    prof = request.user.get_profile()
    if prof.instance:
        instance = prof.instance
    elif request.user.is_staff or request.user.is_superuser:
        #looks like `latest` qs method is broken in django-nani
        #applying a workaround for now.
        #TODO fix
        instance = Instance.objects.untranslated().latest()
        #instance = _fake_latest(Instance, Instance.objects.all())#.active())

    last_mission = None
    if instance and instance.missions.count():
        #looks like `latest` qs method is broken in django-nani
        #applying a workaround for now.
        #TODO fix
        #last_mission = _fake_latest(Mission, instance.missions)
        last_mission = Mission.objects.untranslated().order_by('pk')[0]

    page = request.GET.get('page', 1)
    
    # Dashboard related forms
    activation_form = ActivationForm()

    # Handle the last bit of interaction necessary to fully set up an account.
    # This step ensures they have entered in a first/last name and accepted terms/research.
    if request.method == 'POST':
        activation_form = ActivationForm(request.POST)

        if activation_form.is_valid():
            prof = request.user.get_profile()
            prof.accepted_term = activation_form.cleaned_data['accepted_term']
            prof.accepted_research = activation_form.cleaned_data['accepted_research']
            #TODO: is_of_age is now deprecated!
            prof.is_of_age = True;
            prof.save()

            user = request.user
            user.is_active = True
            user.save()

            ActivityLogger().log(request.user, request, 'account', 'created', '/player/'+ str(user.id), 'profile')
            PointsAssigner().assign(request.user, 'account_created')

            return HttpResponseRedirect(reverse('accounts:dashboard'))
    
    # List all users following for filtering the activity feed later on.
    feed = []
    for user in prof.following.all():
        feed.append(user)
    feed.append(request.user)

    # Fetch activity log feed for dashboard.
    log = Activity.objects.filter(instance=instance).order_by('-date')[:9]
    missions = instance and instance.missions.active() or Mission.objects.none()
    activities = PlayerActivity.objects.none()
    
    if (missions.count() > 0):
        mission = missions[0]
        activities = PlayerActivity.objects.distinct().filter(mission=mission)
        #activities = activities.filter(Q(answers__isnull=True)|Q(answers__answerUser=request.user))

    completed_challenges = PlayerChallenge.objects.completed().filter(player=request.user)
    challenges = instance and instance.challenges.active().exclude(player_challenges__in=completed_challenges) or Challenge.objects.none()

    paginator = Paginator(activities, 5)
    activities_page = paginator.page(page)

    leaderboard = UserProfile.objects.filter(instance=instance).order_by('-totalPoints')[:20]

    #import ipdb;ipdb.set_trace()

    return HttpResponse(tmpl.render(RequestContext(request, {
        'activation_form': activation_form,
        'log': log,
        'last_mission': last_mission,
        'paginator': paginator,
        'activities_page': activities_page,
        'challenges': challenges,
        'leaderboard': leaderboard,
        'instance': instance
    })))
