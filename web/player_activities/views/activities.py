from operator import itemgetter

from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required

from PIL import Image

from answers.models import *
from comments.models import *
from comments.forms import *
from player_activities.forms import *
from player_activities.models import *
from player_activities.views import _get_activity, getComments, comment_fun,\
    log_activity
from reports.actions import *

from django.db.models import get_model

def _build_context(action, activity, user=None):
    
    context = {}

    def _get_related():        
        #FIX_ME: it returns singleresponse_abswers for open_ended activity!
        # Because multi, open and single are of PlayerActivity class.
        
        #for klass in ['AnswerEmpathy', 'AnswerMap', 'AnswerSingleResponse', 
        #              'AnswerMultiResponse', 'AnswerOpenEnded']:
        #    related_name = klass.replace('Answer', '').lower() + '_answers'
        #    if hasattr(activity, related_name):
        #        return getattr(activity, related_name)
        
        # Quick fix:
        if activity.type.type == 'open_ended':
            return getattr(activity, 'openended_answers')
        elif activity.type.type == 'multi_response':
            return getattr(activity, 'multiresponse_answers')
        else:
            for klass in ['AnswerEmpathy', 'AnswerMap', 'AnswerSingleResponse']:
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
                        my_comments =myAnswer.comments.all().order_by('-posted_date')
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
                for user, data in sorted(answer_dict.items()):
                    all_answers.append((user, mark_safe('<ul>' + ''.join(data['answers']) + '</ul>'), data['comments']))
                if user:
                    my_answers = mark_safe('<ul>' + ''.join(answer_dict[user]['answers']) + '</ul>')
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
                markers = simplejson.loads("%s" % map)["markers"]
                for coor in markers if markers != None else []:
                    coor = coor["coordinates"]
                    init_coords.append( [x, coor[0], coor[1]] )
                    x = x + 1

            if not map:
                map = activity.mission.instance.location
            context.update(dict(
                init_coords = init_coords,
                map = map,
            ))

    elif action in ['play', 'replay']:
        if (activity.type.type == "open_ended"):
            form = make_openended_form()
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
        elif activity.type.type == "empathy":
            form = make_empathy_form()         
                
        context.update({'form': form})

    return context


def _get_mcqs(activity):
    return MultiChoiceActivity.objects.language(get_language()).filter(activity=activity).order_by('id')


def _get_mc_choices(activity):
    return _get_mcqs(activity).values_list('pk', 'value')


def _get_mc_choice_ids(activity):
    return _get_mcqs(activity).values_list('pk', flat=True)


def activity(request, activity_id, template=None, **kwargs):
    model = kwargs.pop('model')
    action = kwargs.pop('action')
    activity = _get_activity(activity_id, get_model(*(model.split('.'))))
    if not activity:
        raise Http404("unknown activity type")

    if action=='replay' and activity.mission.is_expired():
        return HttpResponseRedirect(activity.get_overview_url())

    if action=='play' and activity.is_completed(request.user):
        return HttpResponseRedirect(activity.get_overview_url())

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
            if comment_form.errors:
                errors.update(comment_form.errors)        
        context.update({'errors': errors})
            
    def _is_form_valid():
        is_valid = form.is_valid()        
        if action == 'replay':
            return is_valid
        return is_valid and comment_form.is_valid()
            
    if request.method == "POST":       
        
        if action in ['play', 'replay']:
            answer = None
            if request.POST["form"] == "open_ended":               
                form = make_openended_form()(request.POST)                
                if _is_form_valid():
                    response_message = form.cleaned_data.get('response_message', '')
                    try:
                        answer = AnswerOpenEnded.objects.get(activity=activity,
                                                             answerUser=request.user)
                        answer.comment = response_message
                        answer.save()
                    except AnswerOpenEnded.DoesNotExist:
                        answer = AnswerOpenEnded.objects.create(
                                                activity=activity,
                                                answerUser=request.user,
                                                comment=response_message)                                
                else:
                    _update_errors()
            elif request.POST["form"] == "single_response":                
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
            elif request.POST["form"] == "empathy":                              
                form = make_empathy_form()(request.POST)
                if _is_form_valid():
                    response_message = form.cleaned_data.get('response_message', '')
                    try:
                        answer = AnswerEmpathy.objects.get(activity=activity,
                                                           answerUser=request.user)
                        answer.comment = response_message
                        answer.save()
                    except AnswerEmpathy.DoesNotExist:
                        answer = AnswerEmpathy.objects.create(
                                                activity=activity,
                                                answerUser=request.user,
                                                comment=response_message)                                
                else:
                    _update_errors()                
        
            if answer is not None:
                if action == 'replay':
                    return log_activity(request, activity, "replayed")
                elif action == 'play':
                    comment_fun(answer, comment_form, request)
                    PointsAssigner().assignAct(request.user, activity)
                    return log_activity(request, activity, "completed")
        elif action == "overview":            
            if comment_form.is_valid():
                comment = Comment.objects.create(
                                    content_object=activity,
                                    message=comment_form.cleaned_data['message'], 
                                    user=request.user,
                                    instance=activity.mission.instance,
                )
                if request.POST.has_key('yt-url'):
                    if request.POST.get('yt-url'):
                        comment.attachment.create(
                            file=None,
                            url=request.POST.get('yt-url'),
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
    if not(activity.mission.is_future() or activity.mission.is_expired()):
        user = request.user
    ctx = _build_context(action, activity, user=user )
    context.update(ctx)
    template = "player_activities/" + activity.type.type
    if action == 'play':
        template = template + "_response.html"
    elif action in ['replay', 'overview']:
        template= "".join([template, "_", action, ".html"])

    print context

    return render_to_response(template, RequestContext(request, context))
