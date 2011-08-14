import datetime
import math
import re

from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, RequestContext, loader
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext as _

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from web.accounts.forms import *
from web.accounts.models import UserProfile
from web.answers.models import Answer
from web.challenges.models import Challenge, PlayerChallenge
from web.comments.forms import CommentForm
from web.instances.models import Instance
from web.missions.models import Mission
from web.player_activities.models import PlayerActivity
from web.reports.actions import ActivityLogger, PointsAssigner
from web.reports.models import Activity
from web.values.models import *


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

def register(request):
    def valid(firstName, lastName, email, password, form):
        player = User.objects.create(email=email)
        player.first_name = firstName
        player.last_name = lastName
        player.set_password(password)
        player.is_active = True
        player.save()
        player = auth.authenticate(username=email, password=password)
        auth.login(request, player)
        player.save()
        uinfo = player.get_profile()
        uinfo.instance = form.cleaned_data['instance']
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
        
        return HttpResponseRedirect(reverse('accounts_dashboard'))

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
    def valid(firstName, lasstName, email, password, form):
        # Send a new password and update account
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        send_mail(_('Password Changed'), _('Your temporary password is: %(password)s') % { 'password': password }, settings.NOREPLY_EMAIL, [email])
        messages.success(request, _('A temporary password has been sent to your email address.'))

        return HttpResponseRedirect(reverse('accounts_login'))
        
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
                                            'email': profile.user.email if profile.user.email != None else "",
                                            'birth_year': profile.birth_year if profile.birth_year != None else "",
                                            
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
                if (request.POST.get('email', None) == None or request.POST.get('email', None) == ''):
                    profile.user.email = None
                else:
                    profile.user.email = profile_form.cleaned_data['email']
                
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

                return HttpResponseRedirect('/dashboard')
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
    player = User.objects.get(id=id)
    
    instance = player.get_profile().instance
    log = Activity.objects.filter(instance=instance, user=player).order_by('-date')[:6]

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = player.get_profile().comments.create(
                message=comment_form.cleaned_data['message'], 
                user=request.user,
                instance=instance,
            )

            if request.POST.has_key('yt-url'):
                url = request.POST.get('yt-url')
                if url:
                    comment.attachment.create(
                        file=None,
                        url=url,
                        type='video',
                        user=request.user,
                        instance=request.user.get_profile().instance,
                    )

            if request.FILES.has_key('picture'):
                comment.attachment.create(
                    file=request.FILES.get('picture'),
                    user=request.user,
                    instance=request.user.get_profile().instance,
                )

            return HttpResponseRedirect(reverse('accounts_profile', args=[id]))

    followingme = []

    for p in User.objects.select_related():
        try:
            if player and player.get_profile() and player in p.get_profile().following.all():
                followingme.append(p)
        except:
            pass

    
    
    value_wrapper = []
    playervalues = PlayerValue.objects.filter(user=player)
    
    values = Value.objects.filter(instance=instance)
    total_coins = 0
    for value in values:
        total_coins += value.coins
    
    total_playerCoins = 0
    for value in values:
        player_value = playervalues.filter(value=value)
        coins = value.coins
        if len(player_value) > 0:
            total_playerCoins += player_value[0].coins
            # +0.0 coerces to a float for percentages
            value_wrapper.append({ 'value': value, 'coins': coins, 'player_coins': player_value[0].coins, 
                                  'percent': 0 if total_coins == 0 else ((coins+0.0)/total_coins)*100 })
        else:
            value_wrapper.append({ 'value': value, 'coins': coins, 'player_coins': 0,
                                   'percent': 0 if total_coins == 0 else ((coins+0.0)/total_coins)*100 })    
    
    tmpl = loader.get_template('accounts/profile.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'player': player,
        'followingme': followingme,
        'log': log,
        'total_playerCoins': total_playerCoins,
        'value_wrapper': value_wrapper,
    })))

@login_required
def follow(request, id):
    u = User.objects.get(id=id)
    request.user.get_profile().following.add( u )
    ActivityLogger().log(request.user, request, u.get_profile().first_name, 'started following', '/player/'+ id, 'profile')

    return HttpResponseRedirect('/player/'+ str(id))

@login_required
def unfollow(request, id):
    request.user.get_profile().following.remove( User.objects.get(id=id) )

    return HttpResponseRedirect('/player/'+ str(id))

@login_required
def dashboard(request):
    tmpl = loader.get_template('accounts/dashboard.html')

    instance = None

    profile = request.user.get_profile()
    if profile.instance:
        instance = profile.instance
    elif request.user.is_staff or request.user.is_superuser:
        instances = Instance.objects.active()
        if instances.count():
            instance = instances.latest()

    last_mission = None
    if instance and instance.missions.count():
        last_mission = instance.missions.latest()

    page = request.GET.get('page', 1)
    
    # Dashboard related forms
    activation_form = ActivationForm()

    # Handle the last bit of interaction necessary to fully set up an account.
    # This step ensures they have entered in a first/last name and accepted terms/research.
    if request.method == 'POST':
        activation_form = ActivationForm(request.POST)

        if activation_form.is_valid():
            profile = request.user.get_profile()
            profile.accepted_term = activation_form.cleaned_data['accepted_term']
            profile.accepted_research = activation_form.cleaned_data['accepted_research']
            #TODO: is_of_age is now deprecated!
            profile.is_of_age = True;
            profile.save()

            user = request.user
            user.is_active = True
            user.save()

            ActivityLogger().log(request.user, request, 'account', 'created', '/player/'+ str(user.id), 'profile')
            PointsAssigner().assign(request.user, 'account_created')

            return HttpResponseRedirect(reverse('accounts_dashboard'))
    
    # List all users following for filtering the activity feed later on.
    feed = []
    for user in profile.following.all():
        feed.append(user)
    feed.append(request.user)

    # Fetch activity log feed for dashboard.
    log = Activity.objects.filter(instance=instance).order_by('-date')[:9]
    missions = instance and instance.missions.active() or Mission.objects.none()
    activities = PlayerActivity.objects.none()
    
    if (missions.count() > 0):
        mission = missions[0]
        activities = PlayerActivity.objects.distinct().filter(mission=mission)
        activities = activities.filter(Q(answers__isnull=True)|Q(answers__answerUser=request.user))

    completed_challenges = PlayerChallenge.objects.completed().filter(player=request.user)
    challenges = instance and instance.challenges.active().exclude(player_challenges__in=completed_challenges) or Challenge.objects.none()

    paginator = Paginator(activities, 5)
    activities_page = paginator.page(page)

    leaderboard = UserProfile.objects.filter(instance=instance).order_by('-totalPoints')[:20]

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
