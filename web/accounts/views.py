import datetime
import urlparse

from stream.models import Action

from localeurl.models import reverse
from localeurl.utils import strip_path, locale_path

from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import HttpResponse, Http404, HttpResponseServerError
from django.shortcuts import get_object_or_404, render, redirect
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

from PIL import Image

from web.accounts.forms import *
from web.accounts.models import Notification, UserProfile
from web.answers.models import Answer
from web.challenges.models import Challenge, PlayerChallenge
from web.comments.forms import CommentForm
from web.instances.models import Instance
from web.missions.models import Mission
from web.player_activities.models import PlayerActivity, PlayerEmpathyActivity, PlayerMapActivity
from web.reports.models import Activity
from web.values.models import *
from web.core.utils import _fake_latest, instance_from_request

import logging
log = logging.getLogger(__name__)

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
        form = authentication_form(request, data=request.POST)
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
            user = form.get_user()
            log.debug('logged in: %s <%s>' % (str(user), user.email))

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            lang = user.get_profile().preferred_language
            # set the game we are logging the user into
            #
            current_game = form.cleaned_data.get('instance')
            request.session['current_game_slug'] = current_game.slug

            if lang in dict(settings.LANGUAGES).keys():
                spath = strip_path(redirect_to)[1]
                return redirect(
                        "".join(
                                [
                                    current_game.get_absolute_url(ssl=not(settings.DEBUG)),
                                    locale_path(spath, lang)
                                ]
                        ),
                        permantent=True,
                )

            return redirect(
                    "".join([
                                current_game.get_absolute_url(ssl=not(settings.DEBUG)), 
                                redirect_to
                            ]
                    ),
                        permantent=True,
            )
        else:
            log.debug('form invalid %s' % form.errors)
            print('form invalid %s' % form.errors)

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
    return render(render, template_name, context)



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

    return render(request, 'accounts/notifications.html', data)

# Forgot your password
def forgot(request):
    def valid(firstName, lastName, email, password, form):
        # Send a new password and update account
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        send_mail(_('Password Changed'), _('Your temporary password is: %(password)s') % { 'password': password }, settings.NOREPLY_EMAIL, [email])
        messages.success(request, _('A temporary password has been sent to your email address.'))

        return redirect(reverse('accounts:login'))

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
        raise Http404("could not locate a user profile")

    change_password_form = ChangePasswordForm()
    profile_form = UserProfileForm(instance=profile,
                                   initial={
                                        'first_name': profile.user.first_name if profile.user.first_name is not None else "",
                                        'last_name': profile.user.last_name if profile.user.last_name is not None else "",
                                        'email': profile.email if profile.email is not None else "",
                                        'birth_year': profile.birth_year if profile.birth_year is not None else "",
                                        'preferred_language': profile.preferred_language,
                                        #'affiliations': profile.affils.values_list('pk', flat=True), 
                                    }
    )
    if request.method == 'POST':
        # Change password form moved to user profile
        if request.POST['form'] == 'change_password':
            change_password_form = ChangePasswordForm(request.POST)
            if change_password_form.is_valid():
                password = change_password_form.cleaned_data['password']
                confirm = change_password_form.cleaned_data['confirm']

                request.user.set_password(confirm)
                request.user.save()
                messages.success(request, "Your new password was saved.")
        else:
            # User profile form updated, not change password
            profile_form = UserProfileForm(data=request.POST, files=request.FILES, instance=profile)
            if profile_form.is_valid():
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


                profile.affils = profile_form.cleaned_data.get('affiliations')
                aff_other = profile_form.cleaned_data.get('affiliations_other')
                if aff_other != '':
                    for a in aff_other.split(','):
                        aff, created = Affiliation.objects.get_or_create(name=a.strip())
                        aff.save()
                        profile.affils.add(aff)

                profile.user.save()

                if request.FILES.get('avatar', None) != None:
                    profile.avatar = request.FILES['avatar']
                profile.save()
                profile_form.save()

                return redirect(reverse('accounts:dashboard'))

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
    instance = instance_from_request(request)
    #log = Activity.objects.filter(instance=instance, user=player).order_by('-date')[:6]    

    stream = Action.objects.get_for_actor(player)
    comment_form = CommentForm(data=request.POST or None)

    if request.method == 'POST':        
        if comment_form.is_valid():           
            comment = profile.comments.create(
                content_object=profile,                 
                user=request.user,
                instance=instance,
                message = u'%s' % comment_form.cleaned_data['message']
            ) 
            comment.save()

            if request.user != player:
                message = "%s commented on your profile" % (
                    request.user.get_profile().screen_name
                )
                player.notifications.create(content_object=profile, message=message)

            if request.POST.has_key('video-url'):
                url = request.POST.get('video-url')
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
            return redirect(reverse('accounts_profile', args=[id]))


    values = Value.objects.filter(instance=instance)
    community_spent = values.aggregate(Sum('coins'))['coins__sum'] or 0

    value_wrapper = []
    player_values = PlayerValue.objects.filter(user=player)

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
        'stream': stream,
        'player_spent': player_spent,
        'value_wrapper': value_wrapper,
    })))

@login_required
def dashboard(request, template_name='accounts/dashboard.html'):
    # expecting the current game to be 
    # set by middleware
    if hasattr(request, 'current_game'):
        instance = request.current_game
    else:
        raise Http404("could not locate a valid game")

    page = request.GET.get('page', 1)

    # Fetch activity log feed for dashboard.
    missions = instance and instance.missions.active() or Mission.objects.none()

    #if missions.count():
    #    log = Activity.objects.filter(instance=instance).order_by('-date')[:9]
    #else:
    #log = Activity.objects.filter(instance=instance, type='official_response').order_by('-date')[:9]
    STREAM_LENGTH = 10
    if not instance.is_expired():
        stream_kwargs = {}
        if request.user.is_superuser:
            STREAM_LENGTH = 50
        else:
            #compile a list of exceptions
            users_for_instance =  UserProfilePerInstance.objects.filter(instance=instance).values_list('user_profile__user__pk', flat=True)
            stream_kwargs.update(dict(
                    # - do not show comments
                    #action_object_comment__isnull=True
                    verb__in=[
                        'challenge_completed',
                        'challenge_created',
                        'activity_completed',
                        'activity_replayed',
                        'activity_official_response_created',
                        'token_spent',
                    ],
                    actor_user__pk__in=users_for_instance,
            ))
        stream = Action.objects.filter(**stream_kwargs)
    else:
        stream = Action.objects.filter(verb='activity_official_response_created')

    stream = stream.order_by('-datetime')[:STREAM_LENGTH]

    activities = PlayerActivity.objects.none()

    if (missions.count() > 0):
        mission = missions[0]
        activities = []
        for model_klass in [PlayerActivity, PlayerEmpathyActivity, PlayerMapActivity]:
            activities.extend(list(model_klass.objects.filter(mission=mission)))
        activities = sorted(activities, key=lambda a: (a.is_completed(request.user), a.name))

    completed_challenges = PlayerChallenge.objects.completed().filter(player=request.user)
    challenges = instance and instance.challenges.active().exclude(player_challenges__in=completed_challenges) or Challenge.objects.none()

    completed = []
    for activity in activities:
        if activity.is_completed(request.user):
            completed.append(activity)

    paginator = Paginator(activities, 5)
    activities_page = paginator.page(page)

    affboard = []
    #for a in Affiliation.objects.filter(instance=instance):
    #   points = a.userprofile_set.all().aggregate(Sum('totalPoints'))['totalPoints__sum'] or 0
    #   affboard.append((points, a))
    #ffboard.sort()
    #ffboard.reverse()

    context = dict(
        stream = stream,
        paginator = paginator,
        activities_page = activities_page,
        completed = completed,
        challenges = challenges,
        leaderboard = [], #UserProfile.objects.filter(instance=instance).order_by('-totalPoints')[:20],
        instance = instance,
        affiliations_leaderboard = affboard[:20],
    )
    return render(request, template_name, context)


@login_required
def admin_instance_email(request, instance_id=None):
    if not request.user.is_superuser:
        return
    instance = Instance.objects.untranslated()[0]
    email_form = AdminInstanceEmailForm()
    tmpl = loader.get_template("accounts/instance_email.html")
    return HttpResponse(tmpl.render(RequestContext(request, { 
             "form": email_form,
             "instance": instance,
             "instance": instance,
             })))

@login_required
def admin_sendemail(request):
    if not request.user.is_superuser:
        return

    if (request.method != "POST"):
        return HttpResponseServerError("The request method was not POST")
    s = ""
    for x in request.POST:
        s = "%s%s: %s<br>" % (s, x, request.POST[x])

    instance = Instance.objects.untranslated().get(id=int(request.POST["instance_id"]))
    form = AdminInstanceEmailForm(request.POST)
    if form.is_valid():
        body = form.cleaned_data["email"]
        subject = form.cleaned_data["subject"]
        emailList = []
        ups = UserProfile.objects.filter(instance=instance, receive_email=True)
        for up in ups:
            send_mail(subject, body, settings.NOREPLY_EMAIL, [up.user.email], fail_silently=False)
        return redirect(reverse("home"))

    tmpl = loader.get_template("accounts/instance_email.html")
    return HttpResponse(tmpl.render(RequestContext(request, { 
             "form": form,
             "instance_value": instance,  
             }, 
            #[ip]
            )))
