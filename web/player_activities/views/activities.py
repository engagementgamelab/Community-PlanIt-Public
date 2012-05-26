from sijax import Sijax
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

from web.core.utils import missions_bar_context
from web.answers.models import *
from web.missions.models import Mission
from web.comments.models import *
from web.comments.forms import *
from ..forms import *
from ..models import *
from ..views import _get_activity, comment_fun,\
    log_activity_and_redirect

from django.db.models import get_model

import logging
log = logging.getLogger(__name__)

def _build_context(request, action, activity, user=None):

    context = {}
    activity_type = activity.activity_type_readable

    def _get_related():        
        if activity_type == 'open_ended':
            return getattr(activity, 'openended_answers')
        elif activity_type == 'empathy':
            return getattr(activity, 'empathy_answers')
        elif activity_type == 'multi_response':
            return getattr(activity, 'multichoice_answers')
        else:
            for klass in ['AnswerMap', 'AnswerSingleResponse']:
                related_name = klass.replace('Answer', '').lower() + '_answers'
                if hasattr(activity, related_name):
                    return getattr(activity, related_name)

    if action == 'overview':

        create_comment_sijax = Sijax()
        create_comment_sijax.set_request_uri(reverse('comments:ajax-create'))
        context.update(
                {
                    'create_comment_sijax_js' : create_comment_sijax.get_js(),
            }
        )

        if activity_type != 'multi_response':
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

        if activity_type in ['multi_response', 'single_response']:
            choices = MultiChoiceActivity.objects.by_activity(activity=activity)
            context.update({'choices': choices})

            if activity_type == "multi_response":
                answers = AnswerMultiChoice.objects.answers_by_activity(activity)
                my_comment = None
                my_answers = None
                answer_dict = {}
                for answer in answers:
                    answer_user  = answer.get_user()
                    if not answer_dict.has_key(answer_user):
                        answer_dict[answer_user] = {'answers': [], 'comments': []}
                    answer_dict[answer_user]['answers'].append('<li>%s</li>' % answer.option_value)
                    for comment in answer.comments.all():
                        if user:
                            if not my_comment:
                                my_comment = comment
                        answer_dict[answer_user]['comments'].append(comment)
                all_answers = []
                if user and user in answer_dict:
                    my_answers = mark_safe('<ul>' + ''.join(answer_dict[user]['answers']) + '</ul>')
                for user, data in sorted(answer_dict.items()):
                    all_answers.append((user, mark_safe('<ul>' + ''.join(data['answers']) + '</ul>'), data['comments']))
                #log.debug('overview multi my answers %s' % my_answers)
                #log.debug('overview multi all answers %s' % all_answers)
                #print all_answers
                context.update(
                    dict(
                        all_answers = all_answers,
                        my_answers = my_answers,
                        my_comment = my_comment
                    )
                )
        elif activity_type == 'map':
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
        if activity_type == 'open_ended':
            form = make_openended_form()
        elif activity_type == 'empathy':
            form = make_empathy_form()
        elif (activity_type == "single_response"):
            choices = _get_mc_choices(activity)
            form = make_single_form(choices)
        elif (activity_type == "multi_response"):
            choices = _get_mc_choices(activity)
            form = make_multi_form(choices)
        elif (activity_type == "map"):
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
def activity(request, activity_id, template=None, **kwargs):
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
            activity_completed_verb = "activity_completed"
            form_name = request.POST["form"] 

            if form_name == "single_response":
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
            elif form_name == "multi_response":
                choices = _get_mc_choices(activity)
                form = make_multi_form(choices)(request.POST)
                if _is_form_valid():
                    #this gets very very messy....

                    #cleans out all of the choices that the user selected from the check boxes

                    my_answers = AnswerMultiChoice.objects.answers_by_activity(activity).\
                                            filter(user=request.user)
                    for answer in my_answers:
                        amc.comments.clear()
                    my_answers.delete()

                    first_found = False
                    for key in request.POST.keys():
                        if key.find("response_") >= 0:
                            multi_choice_option = MultiChoiceActivity.objects.get(
                                                        id=int(request.POST[key])
                                                    )
                            #This is tricky, the reponse: value returned object is response_$(id): id
                            #So basically if the response exists it means that checkbox was checked and the
                            # value returned will be the ID and will always be an int
                            new_answer = AnswerMultiChoice.objects.create(
                                                    user = request.user,
                                                    option = multi_choice_option,
                            )
                            #Yes it's a hack, only make a comment for the first response
                            if not first_found:
                                answer = new_answer
                                first_found = True
                else:
                    _update_errors()
            elif form_name == "map":
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

            elif form_name == "open_ended":
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
                    action_msg = 'replayed'
                elif action == 'play':
                    if activity.type.type in ['open_ended', 'empathy']:
                        comment_fun(answer, request, None, message=form.cleaned_data.get('response', ''))
                    else:
                        comment_fun(answer, request, comment_form)
                    action_msg = 'completed'
                return log_activity_and_redirect(request, activity, action_msg)

    user = None
    if activity.mission.is_active and not request.user.is_superuser:
        user = request.user

    context.update(_build_context(request, action, activity, user=user))
    # this line here updates the context with 
    # mission, my_points_for_mission and progress_percentage
    context.update(missions_bar_context(request, activity.mission))

    template = "player_activities/" + activity.type.type

    if action == 'play':
        template = template + "_response.html"
    elif action in ['replay', 'overview']:
        template= "".join([template, "_", action, ".html"])
    return render_to_response(template, RequestContext(request, context))





