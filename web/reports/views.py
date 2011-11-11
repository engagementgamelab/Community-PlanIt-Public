import os
from datetime import datetime

from stream.models import Action

from django.http import HttpResponseRedirect
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

#from player_activity.models import *

def render_to_excel(values_list, field_titles=[], to_file=False, filename='report'):
    from datetime import datetime, date
    from django.http import HttpResponse
    import xlwt

    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('untitled')

    default_style = xlwt.Style.default_style

    header_style =xlwt.XFStyle()
    header_background = xlwt.Pattern()
    header_background.pattern = xlwt.Pattern.SOLID_PATTERN
    header_background.pattern_fore_colour = 22

    header_font = xlwt.Font()
    header_font.name = 'Calibri'
    header_font.bold = True
    header_style.pattern = header_background

    datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
    date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')

    for col, val in enumerate(field_titles):
        sheet.write(0, col, val, style=header_style)

    for row, rowdata in enumerate(values_list, start=1):
        for col, val in enumerate(rowdata):
            if isinstance(val, datetime):
                style = datetime_style
            elif isinstance(val, date):
                style = date_style
            else:
                style = default_style

            sheet.write(row, col, val, style=style)

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s.xls' % filename

    if to_file:
        book.save(filename)
        return
    book.save(response)
    return response

def _excel_report(request, field_titles, qs_args):
    """
    - all the most popular comments?  I'd like to see what was liked 3 times or more.
    - one report with all comments, organized by activity.  
    """
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("admin:index"))

    NOW = datetime.now()
    values_list = UserProfile.objects.untranslated().values_list(*qs_args).order_by('-user__date_joined')
    return render_to_excel(values_list, field_titles, NOW.strftime('%Y-%m-%d-%H-%M-'))

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
def report_comments_by_activity2(request):
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

    def fetch_replies(answer, comment):
    	replies = []
        if comment.comments.all().count():
            for res in comment.comments.select_related().all():
                replies.append(
                        (
                            res.pk,
                            answer.mission.title,
                            answer.name,
                            answer.type.type,
                            res.posted_date.strftime('%Y-%m-%d %H:%M'),
                            res.user.pk,
                            "response to %s" %(comment.pk),
                            res.message,
                            res.likes.all().count(),
                        )
                )
                fetch_replies(a, res)
        return replies

    values_list = []
    def update_list(answers):
        for answ in answers.select_related('comments').all():
            for c in answ.comments.select_related('user', 'selected', 'likes').all():
                if a.type.type == 'single_response':
                    answer_value = answ.selected.value
                else:
                    answer_value = ''
                values_list.append(
                        (
                            c.pk, 
                            a.mission.title,
                            a.name, 
                            a.type.type, 
                            c.posted_date.strftime('%Y-%m-%d %H:%M'),
                            c.user.pk,
                            answer_value,
                            c.message, 
                            c.likes.all().count(),
                        )
                )
                if c.comments.all().count():
                    values_list.extend(fetch_replies(a, c))

    for a in PlayerEmpathyActivity.objects.select_related().all():
        update_list(getattr(a, 'empathy_answers'))

    for a in PlayerActivity.objects.select_related().all().order_by('type'):
        if a.type.type == 'open_ended':
            update_list(getattr(a, 'openended_answers'))
        elif a.type.type == 'single_response':
            update_list(getattr(a, 'singleresponse_answers'))

    for a in PlayerMapActivity.objects.select_related().all():
        update_list(getattr(a, 'map_answers'))

    NOW = datetime.now()
    print len(connection.queries)
    return render_to_excel(values_list, field_titles, filename=NOW.strftime('%Y-%m-%d-%H-%M-activity-comments'))

@login_required
def report_comments_popular(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("admin:index"))

    values_list = Comment.objects.annotate(num_likes=Count('likes')).filter(num_likes__gt=2).values_list('user__pk', 'num_likes', 'message').order_by('user__pk')
    NOW = datetime.now()
    return render_to_excel(values_list, field_titles=('user id', 'num of likes', 'message'), filename=NOW.strftime('%Y-%m-%d-%H-%M-popular_comments'))


@login_required
def demographic(request):

    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("admin:index"))

    field_titles = ( 'ID', 'stake', 'race', 'gender', 'education', 'income', 'living', 'affiliations', 'birth year', 'city/neighborhood', 'zip code', 'how discovered?', 'points',)
    values_list = []
    users = UserProfile.objects.exclude(user__is_superuser=True, user__is_staff=True)
    for profile in users:
        all_details = (
                profile.user.pk,
                profile.stake.stake if hasattr(profile, 'stake') and profile.stake is not None else "",
                profile.race.race if hasattr(profile, 'race') and profile.race is not None else "",
                profile.gender.gender if hasattr(profile, 'gender') and profile.gender is not None else "",
                profile.education.education if hasattr(profile, 'education') and profile.education is not None else "",
                profile.income.income if hasattr(profile, 'income') and profile.income is not None else "",
                profile.living.situation if hasattr(profile, 'living') and profile.living is not None else "",
                ", ".join(profile.affils.values_list('name', flat=True)) if hasattr(profile, 'affils') else "",
                profile.birth_year or "",
                profile.city or "",
                profile.zip_code or "",
                profile.how_discovered.how if hasattr(profile, 'how_discovered') and profile.how_discovered is not None else "",
                profile.totalPoints,
        )
        values_list.append(all_details)
        #for c in profile.user.comment_set.all():
        #    values_list.append((profile.user.pk, c.message, '', '', '', ''))
    NOW = datetime.now()
    return render_to_excel(values_list, field_titles, filename=NOW.strftime('%Y-%m-%d-%H-%M-profile_stats'))


@login_required
def demographic2(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("admin:index"))

    field_titles = (
            'ID', 'stake', 'affiliations', 'preferred language', 'picture', 'race', 'gender', 'education', 'income', 'rent/own', 'city/neighborhood', 'zip code', 'points', 'total tokens spent', 'School Environment and Safety', 'Attendance', 'Achievement Gaps', 'Growth', 'Proficiency ', 'Family And Community Engagement', 'Opportunities To Learn',
    )
    values_list = []
    users = UserProfile.objects.exclude(user__is_superuser=True, user__is_staff=True)
    def coins_by_value(user, value_id):
        try:
        	return PlayerValue.objects.get(user=user, value__pk=value_id).coins
        except PlayerValue.DoesNotExist:
        	return 0

    for profile in users:
    	user = profile.user
        all_details = (
                user.pk,
                profile.stake.stake if hasattr(profile, 'stake') and profile.stake is not None else "",
                ", ".join(profile.affils.values_list('name', flat=True)) if hasattr(profile, 'affils') else "",
                profile.preferred_language,
                "Yes" if profile.avatar else "No",
                profile.race.race if hasattr(profile, 'race') and profile.race is not None else "",
                profile.gender.gender if hasattr(profile, 'gender') and profile.gender is not None else "",
                profile.education.education if hasattr(profile, 'education') and profile.education is not None else "",
                profile.income.income if hasattr(profile, 'income') and profile.income is not None else "",
                profile.living.situation if hasattr(profile, 'living') and profile.living is not None else "",
                profile.city or "",
                profile.zip_code or "",
                profile.totalPoints,
                PlayerValue.objects.filter(user=user).aggregate(Sum('coins')).get('coins__sum'),
                #Activity.objects.filter(data='spent token', user=profile.user).count(),
                coins_by_value(user, 173),
                coins_by_value(user, 174),
                coins_by_value(user, 175),
                coins_by_value(user, 176),
                coins_by_value(user, 177),
                coins_by_value(user, 178),
                coins_by_value(user, 179),
        )
        values_list.append(all_details)
        #for c in profile.user.comment_set.all():
        #    values_list.append((profile.user.pk, c.message, '', '', '', ''))
    print len(connection.queries)
    NOW = datetime.now()
    return render_to_excel(values_list, field_titles, filename=NOW.strftime('%Y-%m-%d-%H-%M-profile_stats'))


@login_required
def challenges_activity(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("admin:index"))

    return run_challenges_activity_report()


def run_challenges_activity_report(to_file=False):

    field_titles = (
        'comment id', 'challenge title', 'timestamp', 'user', 'comment', 'likes'
    )
    values_list = []

    def fetch_replies(comment):
        for action in Action.objects.get_for_target(comment):
            if action.verb != 'replied':
                continue
            reply = action.action_object
            values_list.append(
                    (
                        reply.pk,
                        "reply to comment #%s" % comment.pk,
                        action.datetime.strftime('%Y-%m-%d %H:%M'),
                        "%s (%s)" % (action.actor.get_profile().screen_name, action.actor.pk),
                        reply.message,
                        reply.likes.all().count(),
                    )
            )
            fetch_replies(action.action_object)

    for action in Action.objects.filter(verb='challenge_commented'):#.order_by('target_challenge__pk'):
        challenge = action.target.challenge
        comment = action.action_object
        values_list.append(
                (
                    comment.pk,
                    challenge.name,
                    action.datetime.strftime('%Y-%m-%d %H:%M'),
                    "%s (%s)" % (action.actor.get_profile().screen_name, action.actor.pk),
                    comment.message,
                    comment.likes.all().count(),
                )
        )
        fetch_replies(comment)

    print "%s comments" % len(values_list)
    print len(connection.queries)

    NOW = datetime.now()
    filename = NOW.strftime('%Y-%m-%d-%H-%M-challenges-activity')
    if to_file:
        filename = os.path.join('/tmp', filename+'.xls')

    return render_to_excel(values_list, field_titles, to_file, filename)

