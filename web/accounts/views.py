import datetime
import math
import re
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, RequestContext, loader
from django.utils.translation import ugettext as _

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from web.accounts.forms import *
from web.accounts.models import UserProfile
from web.comments.forms import CommentForm
from web.instances.models import Instance
from web.processors import instance_processor as ip
from web.reports.actions import ActivityLogger, PointsAssigner
from web.reports.models import Activity

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
            if request.POST.get('password', None) != None:
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
        try:
            player = User.objects.create(email=email)
            player.first_name = firstName
            player.last_name = lastName
            player.set_password(password)
            player.full_clean()
            player.save()

            tmpl = loader.get_template('accounts/email/welcome.html')
            body = tmpl.render(Context({ 'password': password,
                                        'first_name': firstName }))
        except: pass

        if send_mail(_('New account created!'), body, settings.NOREPLY_EMAIL, [email]):
            messages.success(request, _('Thanks for registering!'))

        player = auth.authenticate(username=email, password=password)
        auth.login(request, player)
        player.save()
        uinfo = player.get_profile()
        uinfo.instance = form.cleaned_data['instance']
        uinfo.coins = 0
        uinfo.points = 0
        uinfo.points_multiplier = 1
        uinfo.username = player.username
        uinfo.email = player.email
        uinfo.generated_password = player.password
        uinfo.first_name = player.first_name;
        uinfo.last_name = player.last_name;
        uinfo.accepted_term = False
        uinfo.accepted_research = False
        uinfo.save()
        return HttpResponseRedirect('/account/dashboard')

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

        return HttpResponseRedirect('/account/login')
        
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
                                            'living': profile.living.id if profile.living != None else 0})
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
                #TODO: Either make email a required field in the database or allow the user to not have an
                # email. (models.py located at web/accounts/models.py)
                if (request.POST.get('email', None) == None or request.POST.get('email', None) == ''):
                    profile.email = None
                else:
                    #TODO: FIX THIS!!!!! THIS IS HORRIBLE!!!!!!! -BMH
                    profile.email = profile_form.cleaned_data['email']
                    profile.user.email = profile_form.cleaned_data['email']
                
                #AND IT CONTINUES, EXPECT BUGS! -bmh
                if (request.POST.get('first_name', None) == None or request.POST.get('first_name', None) == ''):
                    profile.user.first_name = None
                else:
                    profile.user.first_name = profile_form.cleaned_data['first_name']
                    
                if (request.POST.get('last_name', None) == None or request.POST.get('last_name', None) == ''):
                    profile.user.last_name = None
                else:
                    profile.user.last_name = profile_form.cleaned_data['last_name']
                
                #post = ""
                #for x in request.POST:
                #    post = "%s%s: %s<br>" % (post, x, request.POST[x])
                #return HttpResponse(post)
                
                if (request.POST.get("education", None) == None or profile_form.cleaned_data['education'] == "0"):
                    profile.education = None
                else:
                    profile.education = UserProfileEducation.objects.get(id=profile_form.cleaned_data['education'])
                
                if (request.POST.get("income", None) == None or profile_form.cleaned_data['income'] == "0"):
                    profile.income = None
                else:
                    profile.income = UserProfileIncomes.objects.get(id=profile_form.cleaned_data['income'])
                
                if (request.POST.get("living", None) == None or profile_form.cleaned_data['living'] == "0"):
                    profile.living = None
                else:
                    profile.living = UserProfileLiving.objects.get(id=profile_form.cleaned_data['living'])
                
                profile.user.save()
                
              
                if request.FILES.get('avatar', None) != None:
                    profile.avatar = request.FILES['avatar']
                profile.save()
                profile_form.save()
                #This will remove the log message. In the furture look for ActivityLogger.log
                #ActivityLogger.log(request.user, request, 'account profile', 'updated', '/player/'+ str(request.user.id), 'profile')

                if not profile.completed:
                    try:
                        # TODO: Break this out into a function
                        if len(profile.affiliations) and profile.accepted_term and profile.accepted_research and len(profile.phone_number):

                            profile.completed = True
                            profile.save()
                            PointsAssigner.assign(request.user, 'profile_completed')
                    except:
                        pass

                return HttpResponseRedirect('/dashboard')

    tmpl = loader.get_template('accounts/profile_edit.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'profile_form': profile_form,
        'change_password_form': change_password_form,
        'user': request.user,
    },[ip])))

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

    tmpl = loader.get_template('accounts/profile.html')

    return HttpResponse(tmpl.render(RequestContext(request, {
        'player': player,
        'followingme': followingme,
        'log': log,
    },[ip])))

@login_required
def follow(request, id):
    u = User.objects.get(id=id)
    request.user.get_profile().following.add( u )
    ActivityLogger.log(request.user, request, u.get_profile().first_name, 'started following', '/player/'+ id, 'profile')

    return HttpResponseRedirect('/player/'+ str(id))

def unfollow(request, id):
    request.user.get_profile().following.remove( User.objects.get(id=id) )

    return HttpResponseRedirect('/player/'+ str(id))

@login_required
def dashboard(request):
    tmpl = loader.get_template('accounts/dashboard.html')

    profile = request.user.get_profile()
    instance = profile.instance
    
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

            ActivityLogger.log(request.user, request, 'account', 'created', '/player/'+ str(user.id), 'profile')
            PointsAssigner.assign(request.user, 'account_created')

            return HttpResponseRedirect('/account/dashboard')
    
    # List all users following for filtering the activity feed later on.
    feed = []
    for user in profile.following.all():
        feed.append(user)
    feed.append(request.user)

    # Fetch activity log feed for dashboard.
    log = Activity.objects.filter(instance=instance).order_by('-date')[:9]

    return HttpResponse(tmpl.render(RequestContext(request, {
        'activation_form': activation_form,
        'log': log,
    },[ip])))
