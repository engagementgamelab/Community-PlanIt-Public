from PIL import Image

from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
from django.contrib.formtools.wizard import FormWizard

from answers.models import *
from missions.models import Mission
from comments.models import *
from comments.forms import *
from player_activities.forms import *
from player_activities.models import *
from player_activities.views import _get_activity, comment_fun,\
    log_activity_and_redirect
from reports.actions import *

from django.db.models import get_model

import logging
log = logging.getLogger(__name__)

def _build_context(request, action, activity, user=None):

    context = {}

    def _get_related():        
        if activity.type.type == 'open_ended':
            return getattr(activity, 'openended_answers')
        elif activity.type.type == 'empathy':
            return getattr(activity, 'empathy_answers')
        elif activity.type.type == 'multi_response':
            return getattr(activity, 'multichoice_answers')
        else:
            for klass in ['AnswerMap', 'AnswerSingleResponse']:
                related_name = klass.replace('Answer', '').lower() + '_answers'
                if hasattr(activity, related_name):
                    return getattr(activity, related_name)

    if action == 'overview':
        if activity.type.type != 'multi_response':
            answers = activity.__class__.objects.none()
            myAnswer = None
            myComment = None
            related = _get_related()
            if related:
                answers = related.filter(activity=activity)
                if user:
                    try:
                        myAnswer = related.get(activity=activity, answerUser=user)
                        my_comments = myAnswer.comments.all().order_by('posted_date')
                        myComment = None
                        if my_comments.count():
                            myComment = my_comments[0]
                    except: 
                        pass
            context.update(dict(answers=answers, myAnswer=myAnswer, myComment=myComment,))

        if activity.type.type in ['multi_response', 'single_response']:
            choices = MultiChoiceActivity.objects.language(get_language()).filter(activity=activity)
            context.update({'choices': choices})

            if activity.type.type == "multi_response":
                answers = AnswerMultiChoice.objects.filter(option__activity=activity)
                my_comment = None
                my_answers = None
                answer_dict = {}
                for answer in answers:
                    if answer.user not in answer_dict:
                        answer_dict[answer.user] = {'answers': [], 'comments': []}
                    answer_dict[answer.user]['answers'].append('<li>%s</li>' % answer.option.value)
                    for comment in answer.comments.all():
                        if user:
                            if not my_comment:
                                my_comment = comment
                        answer_dict[answer.user]['comments'].append(comment)
                all_answers = []
                if user and user in answer_dict:
                    my_answers = mark_safe('<ul>' + ''.join(answer_dict[user]['answers']) + '</ul>')
                for user, data in sorted(answer_dict.items()):
                    all_answers.append((user, mark_safe('<ul>' + ''.join(data['answers']) + '</ul>'), data['comments']))
                context.update(
                    dict(
                        all_answers = all_answers,
                        my_answers = my_answers,
                        my_comment = my_comment
                    )
                )
        elif activity.type.type == 'map':
            answers = AnswerMap.objects.filter(activity=activity)
            init_coords = []
            x = 0
            map = None
            for answer in answers:
                map = answer.map
                message = None
                if answer.comments.count():
                    message = answer.comments.all()[0].message or None
                player = answer.answerUser.get_profile().screen_name

                markers = simplejson.loads("%s" % map)["markers"]
                for coor in markers if markers != None else []:
                    coor = coor["coordinates"]
                    init_coords.append( [x, coor[0], coor[1], message, player] )
                    x = x + 1

            if not map:
                map = activity.mission.instance.location
            context.update(dict(
                init_coords = init_coords,
                map = map,
            ))

    elif action in ['play', 'replay']:


        if activity.type.type == 'open_ended':
            form = make_openended_form()
        elif activity.type.type == 'empathy':
            form = make_empathy_form()
        elif (activity.type.type == "single_response"):
            choices = _get_mc_choices(activity)
            form = make_single_form(choices)
        elif (activity.type.type == "multi_response"):
            choices = _get_mc_choices(activity)
            form = make_multi_form(choices)
        elif (activity.type.type == "map"):
            form = MapForm()
            init_coords = []
            x = 0
            answer = AnswerMap.objects.filter(activity=activity, answerUser=user)
            if answer.count():
                map = answer[0].map
                markers = simplejson.loads("%s" % map)["markers"]
                x = 0
                for coor in markers if markers != None else []:
                    coor = coor["coordinates"]
                    init_coords.append( [x, coor[0], coor[1]] )
                    x = x + 1
            else:
                map = activity.mission.instance.location
            context.update({'map': map})

        context.update({'form': form})
    
    
    if user:
        context['is_completed'] = activity.is_completed(user)
    # is_completed variable is checked for displaying responses.
    # admin should be able to see the responses even if he had not completed an activity
    if request.user.is_superuser:
        context['is_completed'] = True
    return context

def _get_mcqs(activity):
    return MultiChoiceActivity.objects.language(get_language()).filter(activity=activity).order_by('id')

def _get_mc_choices(activity):
    return _get_mcqs(activity).values_list('pk', 'value')

def _get_mc_choice_ids(activity):
    return _get_mcqs(activity).values_list('pk', flat=True)

@login_required
def activity(request, activity_id, game_header=True, template=None, **kwargs):
    model = kwargs.pop('model')
    action = kwargs.pop('action')
    activity = _get_activity(activity_id, get_model(*(model.split('.'))))
    if not activity:
        raise Http404("unknown activity type")

    if request.user.is_superuser and action != 'overview' :
        return HttpResponseRedirect(activity.get_overview_url())

    if action=='replay' and activity.mission.is_expired():
        return HttpResponseRedirect(activity.get_overview_url())

    if action=='play' and activity.is_completed(request.user):
        return HttpResponseRedirect(activity.get_overview_url())

    comment_form = None
    if activity.type.type not in ['open_ended', 'empathy']:
        comment_form = CommentForm(data=request.POST or None)
    form = None
    errors = {}

    context = dict(
        view_action = action,
        comment_form = comment_form,
        activity = activity,
        errors = errors
    )

    def _update_errors():        
        if form.errors:
            errors.update(form.errors)
        if action != 'replay':        
            if comment_form and comment_form.errors:
                errors.update(comment_form.errors)        
        context.update({'errors': errors})

    def _is_form_valid():
        is_valid = form.is_valid()
        if action == 'replay':
            return is_valid
        if comment_form:
            if not activity.comment_required:
                comment_form.fields['message'].required = False
            return is_valid and comment_form.is_valid()
        return is_valid

    if request.method == "POST":

        if action in ['play', 'replay']:
            answer = None
            if request.POST["form"] == "single_response":
                choices = _get_mc_choices(activity)
                form = make_single_form(choices)(request.POST)
                if _is_form_valid():
                    cd = form.cleaned_data
                    mcactivities = MultiChoiceActivity.objects.filter(id=int(cd.get('response')))
                    if mcactivities.count():
                        selected = mcactivities[0]
                    try:
                        answer = AnswerSingleResponse.objects.get(activity = activity,
                                                                  answerUser = request.user)
                        answer.selected = selected
                        answer.save()
                    except AnswerSingleResponse.DoesNotExist:
                        answer = AnswerSingleResponse.objects.create(
                                   activity = activity,
                                   answerUser = request.user,
                                   selected=selected,
                        )
                else:
                    _update_errors()
            elif request.POST["form"] == "multi_response":
                choices = _get_mc_choices(activity)
                form = make_multi_form(choices)(request.POST)
                if _is_form_valid():
                    #this gets very very messy....

                    choice_ids =  _get_mc_choice_ids(activity)

                    #cleans out all of the choices that the user selected from the check boxes
                    for amc in AnswerMultiChoice.objects.filter(Q(user=request.user) & Q(option__in=choice_ids)):
                        amc.comments.clear()
                    AnswerMultiChoice.objects.filter(Q(user=request.user) & Q(option__in=choice_ids)).delete()
                    first_found = False
                    for key in request.POST.keys():
                        if key.find("response_") >= 0:
                            new_answer = AnswerMultiChoice()
                            new_answer.user = request.user
                            #This is tricky, the reponse: value returned object is response_$(id): id
                            #So basically if the response exists it means that checkbox was checked and the
                            # value returned will be the ID and will always be an int
                            new_answer.option = MultiChoiceActivity.objects.language(get_language()).get(
                                                                            id=int(request.POST[key])
                            )
                            new_answer.save()
                            #Yes it's a hack, only make a comment for the first response
                            if not first_found:
                                answer = new_answer
                                first_found = True
                else:
                    _update_errors()
            elif request.POST["form"] == "map":
                form = MapForm(request.POST)
                if _is_form_valid():
                    map = form.cleaned_data["map"]
                    try:
                        answer = AnswerMap.objects.get(activity=activity, answerUser=request.user)
                    except AnswerMap.DoesNotExist:
                        answer = AnswerMap()
                        answer.activity = activity
                        answer.answerUser = request.user
                    answer.map = map;
                    answer.save()
                else:
                    _update_errors()

            elif request.POST["form"] == "open_ended":
                form = make_openended_form()(request.POST)
                if _is_form_valid():
                    answer, created = AnswerOpenEnded.objects.get_or_create(activity=activity, answerUser=request.user)
                else:
                    _update_errors()
            elif request.POST["form"] == "empathy":
                form = make_empathy_form()(request.POST)
                if _is_form_valid():
                    answer, created = AnswerEmpathy.objects.get_or_create(activity=activity, answerUser=request.user)
                else:
                    _update_errors()

            if answer is not None:
                if action == 'replay':
                    # for open_ended/empathy update the message 
                    # for the submitted comment with the response to the
                    # question
                    if activity.type.type in ['open_ended', 'empathy']:
                        my_comments = answer.comments.all().order_by('posted_date')
                        if my_comments.count():
                            myComment = my_comments[0]
                            myComment.message=form.cleaned_data.get('response', '')
                            myComment.save()
                    return log_activity_and_redirect(request, activity, "replayed")

                elif action == 'play':
                    if activity.type.type in ['open_ended', 'empathy']:
                        comment_fun(answer, request, None, message=form.cleaned_data.get('response', ''))
                    else:
                        comment_fun(answer, request, comment_form)
                    PointsAssigner().assignAct(request.user, activity)
                    return log_activity_and_redirect(request, activity, "completed")

        elif action == "overview":
            if comment_form and comment_form.is_valid():
                comment = Comment.objects.create(
                                    content_object=activity,
                                    message=comment_form.cleaned_data['message'], 
                                    user=request.user,
                                    instance=activity.mission.instance,
                )
                if request.POST.has_key('video-url'):
                    if request.POST.get('video-url'):
                        comment.attachment.create(
                            file=None,
                            url=request.POST.get('video-url'),
                            type='video',
                            user=request.user,
                            instance=activity.mission.instance)
            
                if request.FILES.has_key('picture'):
                    file = request.FILES.get('picture')
                    picture = Image.open(file)
                    if (file.name.rfind(".") -1):
                        file.name = "%s.%s" % (file.name, picture.format.lower())
                    comment.attachment.create(
                        file=request.FILES.get('picture'),
                        user=request.user,
                        instance=activity.mission.instance)
            return HttpResponseRedirect(activity.get_overview_url())

    user = None
    if activity.mission.is_active() and not request.user.is_superuser:
        user = request.user

    ctx = _build_context(request, action, activity, user=user )
    context.update(ctx)
    template = "player_activities/" + activity.type.type

    if action == 'play':
        template = template + "_response.html"
    elif action in ['replay', 'overview']:
        template= "".join([template, "_", action, ".html"])
    context.update({
            'game_header': game_header
    })
    return render_to_response(template, RequestContext(request, context))


class NewActivityWizard(FormWizard):

    def parse_params(self, request, *args, **kwargs):
        self.mission_slug = kwargs.get('mission_slug', '')

    def process_step(self, request, form, step):
        if form.cleaned_data.get('type') == 'multi_response':
            self.form_list = [
                SelectNewActivityForm,
                MultiResponseForm,
            ]
        elif form.cleaned_data.get('type') == 'map':
            self.form_list = [
                SelectNewActivityForm,
                MapForm,
            ]
            mission = Mission.objects.get(slug=self.mission_slug)
            init_coords = []
            map = mission.instance.location
            markers = simplejson.loads("%s" % map)["markers"]
            x = 0
            for coor in markers if markers != None else []:
                coor = coor["coordinates"]
                init_coords.append( [x, coor[0], coor[1]] )
                x = x + 1
            self.extra_context.update(dict(
                init_coords = init_coords,
                map = map,
            ))
            #import ipdb;ipdb.set_trace()
            
    def get_template(self, step):
        log.debug("new activity wizard step %s" % step)
        #import ipdb;ipdb.set_trace()
        if len(self.form_list) > 1:
            if self.form_list[1] == MultiResponseForm:
                print 'multi map'
                return 'player_activities/new_activity_multi.html'
            elif self.form_list[1] == MapForm:
                print 'map'
                return 'player_activities/new_activity_map.html'
        print 'open ended'
        return 'player_activities/new_activity_base.html'

    def done(self, request, form_list):

        form_one = form_list[0]

        type = PlayerActivityType.objects.get( type=form_one.cleaned_data.get('type'))
        mission = Mission.objects.get(slug=self.mission_slug)
        q = form_one.cleaned_data.get('question', '')
        create_kwargs =dict( 
                mission=mission,
                creationUser=request.user,
                type=type,
                question=q,
                name = form_one.cleaned_data.get('name', ''),
        )
        new_activity = PlayerActivity.objects.create(**create_kwargs)
        if len(form_list) == 2:
            form_two = form_list[1]
            for f in  form_two.cleaned_data.keys():
                mc = MultiChoiceActivity.objects.create(
                        value=form_two.cleaned_data.get(f, ''),
                        activity=new_activity,
                )
                print  mc

        return render(request, 'player_activities/new_activity_thanks.html', {
            'mission_slug':self.mission_slug,
        })



