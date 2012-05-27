import os.path
import datetime
import urlparse

from sijax import Sijax

from stream.models import Action
from stream import utils as stream_utils

from localeurl.models import reverse

from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404, HttpResponseServerError
from django.shortcuts import get_object_or_404, render, redirect
from django.template import Context, RequestContext, loader, Template

#from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import get_current_site

from PIL import Image

from .forms import *
from .models import Notification, UserProfile, UserProfileVariantsForInstance
from web.core.utils import missions_bar_context
from web.answers.models import Answer
from web.challenges.models import Challenge, PlayerChallenge
from web.comments.forms import CommentForm
from web.comments.utils import create_video_attachment, create_image_attachment
from web.instances.models import Instance, Affiliation
from web.missions.models import Mission
from web.player_activities.models import PlayerActivity, PlayerEmpathyActivity, PlayerMapActivity
from web.reports.models import Activity
from web.values.models import *

import logging
log = logging.getLogger(__name__)

@csrf_protect
@never_cache
def login_ajax(request, authentication_form=AuthenticationForm):

    def login_process(obj_response, form_data, next=None):
        form = authentication_form(request, data=form_data)
        if form.is_valid():
            auth_login(request, form.get_user())
            user = form.get_user()

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            # set the game we are logging the user into
            #
            current_game = form.cleaned_data.get('instance')
            request.session['current_game_slug'] = current_game.slug
            log.debug('logged in: %s <%s> to %s' % (str(user), user.email, current_game.slug))
            stream_utils.action.send(
                            actor=user,
                            verb='user_logged_in',
                            target=current_game,
                            description='user logged in to system'
            )

            prof_per_instance = UserProfilePerInstance.objects.get(
                        instance=current_game,
                        user_profile=user.get_profile()
            )
            #last_login_datetime  = None
            #my_last_login = prof_per_instance.my_last_login_from_stream()
            #if my_last_login:
            #    last_login_datetime = my_last_login.datetime
            #values_path = None
            #if last_login_datetime is not None and current_game.is_active() \
            #        and last_login_datetime < current_game.start_date:
            #    log.debug('last login on %s redirect %s to map the future' %(last_login_datetime, prof_per_instance.user_profile.screen_name))
                # getting rid of the first slash to be used later with
                # os.path.join
            #    values_path = strip_path(reverse('values:index'))[1][1:]
            #if values_path is not None:
            #    redir = os.path.join(redir, values_path)
            #log.debug("post login redir %s" % redir)

            if next is not None:
                return obj_response.redirect(
                        os.path.join(
                            'https://' if settings.DEBUG == False else 'http://',
                            current_game.for_city.domain,
                            next[1:],
                        )
                )


            active_mission = Mission.objects.default(current_game.pk)
            log.debug("redirecting %s to %s" %(prof_per_instance, active_mission))
            if active_mission:
                return obj_response.redirect(
                            active_mission.get_absolute_url(
                                lang=prof_per_instance.preferred_language
                            )
                )

            return obj_response.redirect(
                    "".join([
                                current_game.get_absolute_url(ssl=not(settings.DEBUG)), 
                                settings.LOGIN_REDIRECT_URL
                            ]
                    ),
            )
        else:
            log.debug('form invalid %s' % form.errors)
            msg = ""
            if form.errors.has_key('__all__'):
                msg = form.errors.get('__all__')[0]
            obj_response.html("div#id_login-form-errors", msg)

    instance = Sijax()
    instance.set_data(request.POST)
    instance.set_request_uri(reverse('accounts:login-ajax'))
    instance.register_callback('login_process', login_process, args_extra=[])
    if instance.is_sijax_request:
        return HttpResponse(instance.process_request())
    return HttpResponse("")

#==========================================================
# only ajax login is enabled at the moment
#
#@csrf_protect
#@never_cache
#def login(request, template_name='registration/login.html',
#          redirect_field_name=REDIRECT_FIELD_NAME,
#          authentication_form=AuthenticationForm,
#          current_app=None, extra_context=None):
#    """
#    Displays the login form and handles the login action.
#    """
#    redirect_to = request.REQUEST.get(redirect_field_name, '')
#
#    if request.method == "POST":
#        form = authentication_form(request, data=request.POST)
#        if form.is_valid():
#            netloc = urlparse.urlparse(redirect_to)[1]
#
#            # Use default setting if redirect_to is empty
#            if not redirect_to:
#                redirect_to = settings.LOGIN_REDIRECT_URL
#
#            # Security check -- don't allow redirection to a different
#            # host.
#            elif netloc and netloc != request.get_host():
#                redirect_to = settings.LOGIN_REDIRECT_URL
#
#            # Okay, security checks complete. Log the user in.
#            auth_login(request, form.get_user())
#            user = form.get_user()
#            log.debug('logged in: %s <%s>' % (str(user), user.email))
#
#            if request.session.test_cookie_worked():
#                request.session.delete_test_cookie()
#
#            lang = user.get_profile().preferred_language
#            # set the game we are logging the user into
#            #
#            current_game = form.cleaned_data.get('instance')
#            request.session['current_game_slug'] = current_game.slug
#
#            if lang.code in dict(settings.LANGUAGES).keys():
#                spath = strip_path(redirect_to)[1]
#                return redirect(
#                        "".join(
#                                [
#                                    current_game.get_absolute_url(ssl=not(settings.DEBUG)),
#                                    locale_path(spath, lang.code)
#                                ]
#                        ),
#                        permantent=True,
#                )
#
#            return redirect(
#                    "".join([
#                                current_game.get_absolute_url(ssl=not(settings.DEBUG)), 
#                                redirect_to
#                            ]
#                    ),
#                        permantent=True,
#            )
#        else:
#            log.debug('form invalid %s' % form.errors)
#
#    else:
#        form = authentication_form(request)
#
#    request.session.set_test_cookie()
#
#    current_site = get_current_site(request)
#
#    context = {
#        'form': form,
#        redirect_field_name: redirect_to,
#        'site': current_site,
#        'site_name': current_site.name,
#    }
#    context.update(extra_context or {})
#    return render(request, template_name, context)



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
    paginator = Paginator(notifications, 20)

    page = request.GET.get('page', 1)
    notifications_page = paginator.page(page)

    context = {
        'paginator': paginator,
        'notifications_page': notifications_page,
    }

    #if request.prof_per_instance:
    #    context['instance'] = request.prof_per_instance
        
    for notification in notifications_page.object_list:
        if notification.read == False:
            notification.unread = True
        notification.read = True
        notification.save()

    context.update(missions_bar_context(request))
    return render(request, 'accounts/notifications.html', context)

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
def edit(request, template_name='accounts/profile_edit.html'):
    try:
        profile = request.user.get_profile()
    except:
        raise Http404("could not locate a user profile")

    if request.user.is_superuser:
        raise Http404("browsing the site as admin user is not supported")

    if not hasattr(request, 'current_game'):
        raise Http404("you are have not property authenticated")



    prof_for_game = UserProfilePerInstance.objects.get(
                                            user_profile=profile,
                                            instance=request.current_game
    )

    change_password_form = ChangePasswordForm()
    profile_form = UserProfileForm(request=request,
                                   initial={
                                        'preferred_language': prof_for_game.preferred_language,
                                        'tagline': profile.tagline,
                                        'affiliations': prof_for_game.affils.all(),
                                        'stakes': prof_for_game.stakes.all(),
                                    }, instance=profile
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
            profile_form = UserProfileForm(request=request, data=request.POST, files=request.FILES, instance=profile)
            if profile_form.is_valid():
                cd = profile_form.cleaned_data
                profile.tagline = cd['tagline']

                if cd.has_key('preferred_language'):
                    prof_for_game.preferred_language = cd.get('preferred_language')

                prof_for_game.stakes = cd.get('stakes')
                prof_for_game.affils = cd.get('affiliations')
                prof_for_game.save()

                if request.FILES.get('avatar', None) != None:
                    profile.avatar = request.FILES['avatar']
                profile.user.save()
                profile.save()
                if cd.get('affiliation_new') != '':
                    affiliation, created = Affiliation.objects.get_or_create(name=cd.get('affiliation_new'))
                    variants = UserProfileVariantsForInstance.objects.get(instance=request.current_game)
                    variants.affiliation_variants.add(affiliation)
                    prof_for_game.affils.add(affiliation)
            else:
                log.debug("edit profile form errors %s: %s" % (profile, profile_form.errors))

        return redirect(reverse('accounts:player_profile', args=(request.user.pk,)))


    context = {
        'profile_form': profile_form,
        'change_password_form': change_password_form,
    }

    context.update(missions_bar_context(request))
    return render(request, template_name, context)

@login_required
def all(request, template='accounts/all.html'):
    profiles_for_game =  UserProfilePerInstance.objects.select_related().filter(instance=request.current_game
        ).exclude(user_profile__user__is_active=False
        ).order_by('-date_created')
    filter_by_variants = Sijax()
    filter_by_variants.set_request_uri(reverse('accounts:ajax-filter-players-by-variant'))

    search_by_kw = Sijax()
    search_by_kw.set_request_uri(reverse('accounts:ajax-search-players-by-kw'))

    context = {
        'profiles_for_game': profiles_for_game,
        'filter_by_variants_form' : FilterPlayersByVariantsForm(request),
        'search_by_kw_form': SearchPlayersByKeywordsForm(request),
        'filter_by_variants_sijax_js' : filter_by_variants.get_js(),
        'search_by_kw_sijax_js': search_by_kw.get_js(),
        'paginate_players_per_page' : settings.ENDLESS_PAGINATE_PLAYERS_PER_PAGE,
    }
    context.update(missions_bar_context(request))

    return render(request, template, context)

def ajax_search(request, search_form, request_uri=None):

    request_uri_for_form = {
        FilterPlayersByVariantsForm: reverse('accounts:ajax-filter-players-by-variant'),
        SearchPlayersByKeywordsForm: reverse('accounts:ajax-search-players-by-kw'),
    }

    def search(obj_response, form_data):
        form = search_form(request, data=form_data)
        if form.is_valid():
            profiles_for_game = form.search()
            context = {
                'profiles_for_game' : profiles_for_game,
                'MEDIA_URL' : settings.MEDIA_URL,
                'STATIC_URL' : settings.STATIC_URL,
                'request': request,
                'paginate_players_per_page' : settings.ENDLESS_PAGINATE_PLAYERS_PER_PAGE,
            }
            players_count_str = "<h3>%s total players</h3>" % profiles_for_game.count()
            obj_response.html("#id_players-count", players_count_str)
            players_tmpl = """
            {% load endless %}
            {% paginate paginate_players_per_page profiles_for_game as players %}
                {% include "accounts/_players_table.html" %}
            """
            t = Template(players_tmpl)
            players_table = t.render(Context(context))
            obj_response.html('#id_players-table', players_table)

            pag_tmpl = """
            {% load endless %}
            {% paginate paginate_players_per_page profiles_for_game %}
                {% include "accounts/_pagination.html" %}
            """
            t = Template(pag_tmpl)
            pagination = t.render(Context(context))
            obj_response.html('div#profile-pagination', pagination)
        else:
            log.debug('find players filter errors: %s', form.errors)

    instance = Sijax()
    instance.set_data(request.POST)
    instance.set_request_uri(request_uri_for_form.get(search_form, ''))
    instance.register_callback('search', search)
    if instance.is_sijax_request:
        return HttpResponse(instance.process_request())

@login_required
def profile(request, id, template_name="accounts/profile.html"):

    if hasattr(request, 'current_game'):
        instance = request.current_game
    else:
        raise Http404("could not locate a valid game")

    context={}
    player = get_object_or_404(User, id=id)
    kwargs={}
    kwargs['instance']=request.current_game
    kwargs['user_profile'] = request.user.get_profile() if request.user == player else player.get_profile()
    try:
        prof_per_instance = UserProfilePerInstance.objects.get(**kwargs)
    except UserProfilePerInstance.DoesNotExist:
        raise Http404("user for this game is not registered")

    if request.method == 'POST':
        this_page = reverse('accounts:player_profile', args=(id,))

        form = CommentForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            log.debug("processed comment_form. cleaned_data: %s" % cd)
            comment_parent  = get_object_or_404(UserProfilePerInstance, id=cd.get('parent_id'))
            comment = comment_parent.comments.create(
                content_object=comment_parent,
                message=cd.get(u'message'),
                user=request.user,
                instance=request.current_game,
            )
            if request.POST.has_key('video-url') and request.POST.get('video-url') != '':
                create_video_attachment(comment, request.POST.get('video-url'), request.current_game, request.user)

            if request.FILES.has_key('picture'):
                create_image_attachment(comment, request.FILES.get('picture'), request.current_game, request.user)

            stream_verb = 'commented'
            stream_utils.action.send(
                            request.user,
                            stream_verb,
                            target=comment_parent,
                            action_object=comment,
                            description="commented on a user profile",
            )
            if request.user != comment_parent.user_profile.user:
                message = '%s commented on your profile.' % request.user.get_profile().screen_name
                comment_parent.user_profile.user.notifications.create(content_object=comment, message=message)

            redirect(
                reverse('accounts:player_profile', 
                        args=(comment_parent.user_profile.user.pk,)
                )
            )

    my_games = Instance.objects.exclude(is_disabled=True).filter(
                    pk__in=
                    UserProfilePerInstance.objects.filter(
                            user_profile = player.get_profile()
                    ).values_list('instance__pk', flat=True)
    )
    stream = Action.objects.get_for_actor( player).\
            exclude(verb='user_logged_in').order_by('-datetime')[:10]


    context.update({
        'player': player,
        'profile_per_instance' : prof_per_instance,
        'stream': stream,
        'affiliations': prof_per_instance.affils.all(),
        'my_games': my_games,
    })
    # this line here updates the context with 
    # mission, my_points_for_mission and progress_percentage
    context.update(missions_bar_context(request))
    return render(request, template_name, context)

"""
@login_required
def ajax_profile_comment_submit(request, prof_per_instance_id):
    files = {}
    sijax_instance = Sijax()
    sijax_instance.set_request_uri(reverse('accounts:ajax-profile-comment-submit', args=(prof_per_instance_id,)))
    register_upload_callback(sijax_instance, 'id_comment-form-'+prof_per_instance_id, profile_comment_handler, args_extra=[files])

    if sijax_instance.is_sijax_request:
        return HttpResponse(sijax_instance.process_request())
"""

@login_required
def dashboard(request, template_name='accounts/dashboard.html'):
# def dashboard(request, template_name='city.html'):
    # expecting the current game to be 
    # set by middleware

    log.debug("dashboard: auth? %s " % request.user.is_authenticated())

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
        active_missions= instance.missions.active(),
        active_future= instance.missions.future(),
        active_past= instance.missions.past(),
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
