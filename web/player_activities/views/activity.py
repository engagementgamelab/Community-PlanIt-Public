from operator import itemgetter

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required

from player_activities.views import (_get_activity, 
                                    getComments, comment_fun, 
                                    _get_translatable_field)
from player_activities.forms import *
from player_activities.models import *
from answers.models import *
from comments.models import *
from comments.forms import *
from reports.actions import *

@login_required
def overview(request, id):

    activities = PlayerActivity.objects.language(get_language()).filter(id=id)

    if activities.count():
        activity = activities[0]
    else:
        raise Http404 ("PlayerActivity with id %s does not exist" % id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
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
            return HttpResponseRedirect(reverse("activities:overview", args=[activity.id]))
    else:
        comment_form = CommentForm()

    context = dict(
            activity = activity,
            comment_form = comment_form,
            view_action = 'overview',
    )

    if activity.type.type == "open_ended":
        answers = AnswerOpenEnded.objects.filter(activity=activity, answerUser=request.user)
        template = 'player_activities/open_overview.html'
        context.update(
            dict(
                answers = answers,
            )
        )

    elif activity.type.type == "single_response":

        choices = MultiChoiceActivity.objects.language(get_language()).filter(activity=activity)
        answers = AnswerSingleResponse.objects.filter(activity=activity)
        myAnswer = answers.filter(answerUser=request.user)
        myComment = None
        if myAnswer.count() > 0:
            myAnswer = myAnswer[0]
            comments = myAnswer.comments.all()
            if comments.count():
                myComment = comments[0]

        template = 'player_activities/single_overview.html'
        context.update(
            dict(
                choices = choices,
                answers = answers,
                myAnswer = myAnswer, 
                myComment = myComment,
            )
        )

    elif activity.type.type == "multi_response":
        choices = MultiChoiceActivity.objects.language(get_language()).filter(activity=activity)
        answers = AnswerMultiChoice.objects.filter(option__activity=activity)

        answer_dict = {}
        for answer in answers:
            if answer.user not in answer_dict:
                answer_dict[answer.user] = {'answers': [], 'comments': []}
            answer_dict[answer.user]['answers'].append('<li>%s</li>' % answer.option.value)
            for comment in answer.comments.all():
                answer_dict[answer.user]['comments'].append(comment)

        print answer_dict

        all_answers = []
        for user, data in sorted(answer_dict.items()):
            all_answers.append((user, mark_safe('<ul>' + ''.join(data['answers']) + '</ul>'), data['comments']))

        template = 'player_activities/multi_overview.html'
        context.update(
            dict(
                choices = choices,
                all_answers = all_answers
            )
        )

    if context and template:
        return render_to_response(template, context, RequestContext(request))
    return HttpResponse("web page not created yet")

@login_required
def activity(request, id, template=None):

    activity = _get_activity(id, PlayerActivity)

    answer_kwargs = dict(activity = activity, answerUser = request.user)
    answers = []
    if (activity.type.type == "single_response"):
        answers = AnswerSingleResponse.objects.filter(**answer_kwargs)
    if (activity.type.type == "open_ended"):
        answers = AnswerOpenEnded.objects.filter()

    if len(list(answers)):
        return HttpResponseRedirect(reverse("activities:overview", args=[activity.id]))

    #answers = Answer.objects.filter(activity=activity, answerUser=request.user)
    #if len(answers) > 0:
    #    return HttpResponseRedirect(reverse("activities:replay", args=[activity.id]))

    #answers = AnswerMultiChoice.objects.filter(option__activity=activity, user=request.user)
    #if len(answers) > 0:
    #    return HttpResponseRedirect(reverse("activities:replay", args=[activity.id]))

    comment_form = CommentForm()
    form = None

    def _get_mc_choices():
        return MultiChoiceActivity.objects.language(get_language()).filter(activity=activity).order_by('id').values_list('pk', 'value')

    def _get_mc_choice_ids():
        return MultiChoiceActivity.objects.language(get_language()).filter(activity=activity).order_by('id').values_list('pk', flat=True)

    if (activity.type.type == "open_ended"):
        form = make_openended_form()
        template = 'player_activities/open_response.html'

    elif (activity.type.type == "single_response"):
        template = 'player_activities/single_response.html'
        choices = _get_mc_choices()
        form = make_single_form(choices)

    elif (activity.type.type == "multi_response"):
        template = 'player_activities/multi_response.html'
        choices = _get_mc_choices()
        form = make_multi_form(choices)

    else:
        raise Http404("unknown activity type")

    errors = {}
    if request.method == "POST":
        #If this game is a replay it should be set below. The reason to not check here
        # is because the type of the game might have changed. If that is the case, the Answer.objects.filteer
        # will exist but it will be the wrong one.  
        comment_form = CommentForm(request.POST)

        if request.POST["form"] == "open_ended":
            template = 'player_activities/open_response.html'
            form = make_openended_form()(request.POST)
            if form.is_valid() and comment_form.is_valid():
                cd = comment_form.cleaned_data
                comment = cd.get('message')
                answer = AnswerOpenEnded.objects.create(
                            activity = activity,
                            answerUser = request.user,
                            comment = comment,
                )
                #comment_fun(answer, comment_form, request)
            else:
                if form.errors:
                    errors.update(form.errors)
                if comment_form.errors:
                    errors.update(comment_form.errors)

        elif request.POST["form"] == "single_response":
            template = 'player_activities/single_response.html'
            choices = _get_mc_choices()
            form = make_single_form(choices)(request.POST)
            if form.is_valid() and comment_form.is_valid():
                cd = form.cleaned_data
                mcactivities = MultiChoiceActivity.objects.filter(id=int(cd.get('response')))
                if mcactivities.count():
                    selected = mcactivities[0]

                answer = AnswerSingleResponse.objects.create(
                            activity = activity,
                            answerUser = request.user,
                            selected=selected,
                )
                comment_fun(answer, comment_form, request)
            else:
                if comment_form.errors:
                    errors.update(comment_form.errors)
                if form.errors:
                    errors.update(form.errors)

        elif request.POST["form"] == "multi_response":
            template = 'player_activities/multi_response.html'
            choices = _get_mc_choices()
            form = make_multi_form(choices)(request.POST)
            if form.is_valid() and comment_form.is_valid():
                #this gets very very messy....

                comment = None
                choice_ids =  _get_mc_choice_ids()

                #cleans out all of the choices that the user selected from the check boxes
                for amc in AnswerMultiChoice.objects.filter(Q(user=request.user) & Q(option__in=choice_ids)):
                    amc.comments.clear()
                AnswerMultiChoice.objects.filter(Q(user=request.user) & Q(option__in=choice_ids)).delete()
                first_found = False 
                for key in request.POST.keys():
                    if key.find("response_") >= 0:
                        answer = AnswerMultiChoice()
                        answer.user = request.user
                        #This is tricky, the reponse: value returned object is response_$(id): id
                        #So basically if the response exists it means that checkbox was checked and the
                        # value returned will be the ID and will always be an int
                        answer.option = MultiChoiceActivity.objects.language(get_language()).get(
                                                                        id=int(request.POST[key])
                        )
                        answer.save()
                        #Yes it's a hack, only make a comment for the first response
                        if not first_found:
                            comment_fun(answer, comment_form, request)
                            first_found = True
                PointsAssigner().assignAct(request.user, activity)
            else:
                if comment_form.errors:
                    errors.update(comment_form.errors)
                if form.errors:
                    errors.update(form.errors)

        ActivityLogger().log(request.user, request, "the activity: " + activity.name[:30] + "...", "completed", reverse("activities:activity", args=[activity.id]), "activity")
        return HttpResponseRedirect(reverse("activities:overview", args=[activity.id]))

    context = dict(
        form = form, 
        comment_form = comment_form,
        errors = errors,
        activity =  activity,
    )
    return render_to_response(template, RequestContext(request, context))

@login_required
def replay(request, id):    
    activity = PlayerActivity.objects.get(id=id)
    form = None
    errors = {}

    if (activity.type.type == "single_response"):
        template = 'player_activities/single_replay.html'
        mc = MultiChoiceActivity.objects.filter(activity=activity)
        choices = []
        for x in mc:
            choices.append((x.id, x.value))
        form = make_single_form(choices)

    elif (activity.type.type == "multi_response"):
        mc = MultiChoiceActivity.objects.filter(activity=activity)
        choices = []
        for x in mc:
            choices.append((x.id, x.value))
        template = 'player_activities/multi_replay.html'
        form = make_multi_form(choices)

    elif (activity.type.type == "open_ended"):
        form = make_openended_form()
        template = 'player_activities/open_replay.html'

    else:
        raise Http404("cannot replay. unknown activity type")

    if request.method == "POST":

        if request.POST["form"] == "open_ended":

            form = make_openended_form()(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                msg = cd.get('message')
                import ipdb;ipdb.set_trace()
                #FIXME
                # there should be one unique answer to replay?
                try:
                    answer = AnswerOpenEnded.objects.get(
                                activity = activity,
                                answerUser = request.user,
                    )
                    answer.comment = msg
                except AnswerOpenEnded.DoesNotExist:
                    answer = AnswerOpenEnded.objects.create(
                                activity = activity,
                                answerUser = request.user,
                                comment = msg,
                    )

                #comment_fun(answer, comment_form, request)
            else:
                if form.errors:
                    errors.update(form.errors)
                if comment_form.errors:
                    errors.update(comment_form.errors)



        if request.POST["form"] == "single_response":
            mc = MultiChoiceActivity.objects.filter(activity=activity)
            choices = []
            for x in mc:
                choices.append((x.id, x.value))
            form = make_single_form(choices)(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                try:
                    answer = AnswerSingleResponse.objects.get(activity=activity, answerUser=request.user)
                    answer.selected = MultiChoiceActivity.objects.get(id=int(cd.get('response')))
                    answer.save()
                except AnswerSingleResponse.DoesNotExist:
                    answer = AnswerSingleResponse.objects.create(
                                                    activity=activity, 
                                                    answerUser=request.user,
                                                    selected = MultiChoiceActivity.objects.get(
                                                                id=int(cd.get('response'))
                                                    )
                    )
            else:
                errors.update(form.errors)

        elif request.POST["form"] == "multi_response":
            mc = MultiChoiceActivity.objects.filter(activity=activity)
            choices = []
            for x in mc:
                choices.append((x.id, x.value))
            form = make_multi_form(choices)(request.POST)
            if form.is_valid():
                #this gets very very messy....
                choices = MultiChoiceActivity.objects.filter(activity=activity)
                ids = []
                for choice in choices:
                    ids.append(choice.id)
                comment = None
                delete_answers = []
                for amc in AnswerMultiChoice.objects.filter(Q(user=request.user) & Q(option__in=ids)):
                    if len(amc.comments.all()) > 0:
                        comment = amc.comments.all()[0]
                    delete_answers.append(amc.pk)

                first_found = False 
                for key in request.POST.keys():
                    if key.find("response_") >= 0:
                        answer = AnswerMultiChoice()
                        answer.user = request.user
                        #This is tricky, the reponse: value returned object is response_$(id): id
                        #So basically if the response exists it means that checkbox was checked and the
                        # value returned will be the ID and will always be an int
                        answer.option = MultiChoiceActivity.objects.get(id=int(request.POST[key]))
                        answer.save()
                        #Yes it's a hack, only make a comment for the first response
                        if not first_found:
                            if comment is not None:
                                comment.content_object = answer
                                comment.save()
                            first_found = True
                AnswerMultiChoice.objects.filter(pk__in=delete_answers).delete()
            else:
                errors.update(form.errors)

        ActivityLogger().log(request.user, request, "the activity: " + activity.name[:30] + "...", "replayed", reverse("activities:activity", args=[activity.id]), "activity")
        return HttpResponseRedirect(reverse("activities:overview", args=[activity.id]))

    context = dict(
        form = form,
        errors = errors,
        activity = activity,
        view_action = 'replay',
    )
    return render_to_response(template, context, RequestContext(request))

