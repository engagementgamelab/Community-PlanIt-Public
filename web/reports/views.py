import os
from datetime import datetime

from stream.models import Action

from django.core.urlresolvers import reverse
from django.db.models import Count
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from accounts.models import UserProfile
from comments.models import Comment
from answers.models import AnswerMultiChoice
from reports.models import Activity
from player_activities.models import PlayerEmpathyActivity, PlayerMapActivity, PlayerActivity
from values.models import *
from django.db.models import Sum

@login_required
def report_comments_by_activity(request):

    field_titles = ('comment id', 'activity type', 'message', 'posted date')
    values_list = []

    def update_list(answers):
        for answ in answers.all():
            for c in answ.comments.all():
                values_list.append((c.pk, a.type.type + ' response' , c.message, c.posted_date.strftime('%Y-%m-%d %H:%M'),))

    for a in PlayerActivity.objects.all().order_by('type'):
        if a.type.type == 'open_ended':
            values_list.append((a.pk, "OPEN ENDED ACTIVITY:", a.question,))
            update_list(getattr(a, 'openended_answers'))
        elif a.type.type == 'multi_response':
                answers = AnswerMultiChoice.objects.filter(option__activity=a)
                for answer in answers:
                    for c in answer.comments.all():
                        values_list.append((c.pk, a.type.type, c.message, c.posted_date.strftime('%Y-%m-%d %H:%M'),))
        elif a.type.type == 'single_response':
            values_list.append((a.pk, "SINGLE RESPONSE ACTIVITY:", a.question,))
            update_list(getattr(a, 'singleresponse_answers'))

    for a in PlayerEmpathyActivity.objects.all():
        values_list.append((a.pk, "EMPATHY ACTIVITY:", a.question,))
        update_list(getattr(a, 'empathy_answers'))

    for a in PlayerMapActivity.objects.all():
        values_list.append((a.pk, "MAP ACTIVITY:", a.question,))
        update_list(getattr(a, 'map_answers'))

    NOW = datetime.now()
    return render_to_excel(values_list, field_titles, filename=NOW.strftime('%Y-%m-%d-%H-%M-comments_by_activity'))

@login_required
def report_comments_by_activity2_multi(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("admin:index"))


    field_titles = ('comment id', 
                    'mission', 
                    'activity title', 
                    'activity type', 
                    'timestamp',
                    'user id',
                    'response code',
                    'comment', 
                    'likes'
    )

    def _fetch_multichoice_replies(answer, comment, mission_title):
    	replies = []
        for res in comment.comments.all():
            replies.append(
                    (
                        res.pk,
                        mission_title,
                        "---",
                        'multichoice',
                        res.posted_date.strftime('%Y-%m-%d %H:%M'),
                        res.user.pk,
                        "response to %s" %(comment.pk),
                        res.message,
                        res.likes.all().count(),
                    )
            )
            _fetch_multichoice_replies(a, res, mission_title=mission_title)
        return replies

    values_list = []

    for a in PlayerActivity.objects.select_related().filter(type__type='multi_response').order_by('mission'):

        answers = AnswerMultiChoice.objects.select_related().filter(option__activity=a)
        for answer in answers:
            for c in answer.comments.all():
                mission_title = answer.option.mission.title
                values_list.append(
                        (
                            c.pk, 
                            mission_title,
                            a.name,
                            'multichoice',
                            c.posted_date.strftime('%Y-%m-%d %H:%M'),
                            c.user.pk,
                            answer.option.value,
                            c.message, 
                            c.likes.all().count(),
                        )
                )
                if c.comments.all().count():
                    values_list.extend(_fetch_multichoice_replies(answer, c, mission_title))

    NOW = datetime.now()
    print len(connection.queries)
    return render_to_excel(values_list, field_titles, filename=NOW.strftime('%Y-%m-%d-%H-%M-activity-comments2_multi'))

@login_required
def activity_report(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("admin:index"))

    from reports.tasks import ActivityReport
    ActivityReport.delay()
    return HttpResponseRedirect(reverse("admin:index"))

@login_required
def comments_popular(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("admin:index"))

    from reports.tasks import PopularCommentsReport
    PopularCommentsReport.delay()
    return HttpResponseRedirect(reverse("admin:index"))

@login_required
def demographic(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("admin:index"))

    from reports.tasks import DemographicReport
    DemographicReport.delay()
    return HttpResponseRedirect(reverse("admin:index"))

@login_required
def challenges_activity(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("admin:index"))

    from reports.tasks import ChallengesReport
    ChallengesReport.delay()
    return HttpResponseRedirect(reverse("admin:index"))
