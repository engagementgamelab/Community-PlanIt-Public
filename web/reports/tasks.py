import os.path
from random import randint
import xlwt
from datetime import datetime, date
from celery.decorators import task
from celery.task import Task
from celery.registry import tasks

from stream.models import Action

from django.http import HttpResponse
from django.contrib.sites.models import Site
from django.db import connection
from django.conf import settings
from django.core.mail import send_mail

from django.core.urlresolvers import reverse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from accounts.models import UserProfile
from comments.models import Comment
from answers.models import AnswerMultiChoice
from reports.models import Activity
from player_activities.models import PlayerEmpathyActivity, PlayerMapActivity, PlayerActivity
from values.models import *
from django.db.models import Sum

import logging
log = logging.getLogger(__name__)

def xls_to_response(xls, fname):
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    xls.save(response)
    return response

class ReportTask(Task):

    values_list = []
    field_titles = []
    notify_subject = None
    id = 0

    def run(self, *args, **kwargs):
        log.debug('ran with %s queries' % len(connection.queries))
        filename = self.render_to_excel()
        log.debug('saved report to %s' %filename)
        self.notify_authors(filename)

    def notify_authors(self, filename):
        subject = "report has been generated. %s" % self.notify_subject
        site = Site.objects.all()[0]
        url = "".join([site.domain, settings.MEDIA_ROOT, 'uploads/reports/',filename])
        body = "report available %s" % url
        send_mail(subject, body, settings.NOREPLY_EMAIL, settings.REPORTS_RECIPIENTS, fail_silently=False)

    def render_to_excel(self, save_to_file=True):

        xls = xlwt.Workbook(encoding='utf8')
        sheet = xls.add_sheet('untitled')

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

        for col, val in enumerate(self.field_titles):
            sheet.write(0, col, val, style=header_style)

        for row, rowdata in enumerate(self.values_list, start=1):
            for col, val in enumerate(rowdata):
                if isinstance(val, datetime):
                    style = datetime_style
                elif isinstance(val, date):
                    style = date_style
                else:
                    style = default_style

                sheet.write(row, col, val, style=style)

        #if not save_to_file:
        #    return xls_to_response(xls, filename)

        NOW = datetime.now()
        filename = "".join([NOW.strftime('%Y-%m-%d-%H-%M'), 
                            "--", str(randint(1000, 10000)), '.xls'])
        location = os.path.join(settings.MEDIA_ROOT, 'uploads/reports', filename)
        xls.save(location)
        print 'saved', location
        return filename


class DemographicReport(ReportTask):

    def run(self, *args, **kwargs):

        self.notify_subject = "Report"

        self.field_titles = (
                'ID', 'stake', 'affiliations', 'preferred language', 'picture', 'race', 'gender', 'education', 'income', 'rent/own', 'city/neighborhood', 'zip code', 'points', 'total tokens spent', 'School Environment and Safety', 'Attendance', 'Achievement Gaps', 'Growth', 'Proficiency ', 'Family And Community Engagement', 'Opportunities To Learn',
        )
        self.values_list = []
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
            self.values_list.append(all_details)
            #for c in profile.user.comment_set.all():
            #    values_list.append((profile.user.pk, c.message, '', '', '', ''))
        super(DemographicReport, self).run(*args, **kwargs)

tasks.register(DemographicReport)


class ChallengesReport(ReportTask):

    def run(self, *args, **kwargs):

        self.notify_subject = "Challenges Report"
        self.field_titles = (
            'comment id', 'challenge title', 'timestamp', 'user', 'comment', 'likes'
        )

        def fetch_replies(comment):
            for action in Action.objects.get_for_target(comment):
                if action.verb != 'replied':
                    continue
                reply = action.action_object
                self.values_list.append(
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
            self.values_list.append(
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

        super(ChallengesReport, self).run(*args, **kwargs)

tasks.register(ChallengesReport)


class PopularCommentsReport(ReportTask):

    def run(self, *args, **kwargs):
        self.notify_subject = "comments by popularity report"
        self.field_titles=('user id', 'num of likes', 'message') 
        self.values_list = Comment.objects.annotate(num_likes=Count('likes')).filter(num_likes__gt=2).values_list('user__pk', 'num_likes', 'message').order_by('user__pk')
        super(PopularCommentsReport, self).run(*args, **kwargs)

tasks.register(PopularCommentsReport)

class ActivityReport(ReportTask):

    def run(self, *args, **kwargs):
        self.notify_subject = "player activity report"
        self.field_titles = ('comment id', 
                            'mission', 
                            'activity title', 
                            'activity type', 
                            'original question',
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
                                '-',
                                res.posted_date.strftime('%Y-%m-%d %H:%M'),
                                res.user.pk,
                                "response to %s" %(comment.pk),
                                res.message,
                                res.likes.all().count(),
                            )
                    )
                    fetch_replies(a, res)
            return replies

        def _fetch_multichoice_replies(answer, comment, mission_title):
            replies = []
            for res in comment.comments.all():
                replies.append(
                        (
                            res.pk,
                            mission_title,
                            "---",
                            'multichoice',
                            '-',
                            res.posted_date.strftime('%Y-%m-%d %H:%M'),
                            res.user.pk,
                            "response to %s" %(comment.pk),
                            res.message,
                            res.likes.all().count(),
                        )
                )
                _fetch_multichoice_replies(a, res, mission_title=mission_title)
            return replies


        def update_list(activity, answers):
            for answ in answers.select_related('comments').all():
                for c in answ.comments.select_related('user', 'selected', 'likes').all():
                    if activity.type.type == 'single_response':
                        answer_value = answ.selected.value
                    else:
                        answer_value = ''

                    self.values_list.append(
                            (
                                c.pk, 
                                activity.mission.title,
                                activity.name, 
                                activity.type.type, 
                                activity.question,
                                c.posted_date.strftime('%Y-%m-%d %H:%M'),
                                c.user.pk,
                                answer_value,
                                c.message, 
                                c.likes.all().count(),
                            )
                    )
                    if c.comments.all().count():
                        self.values_list.extend(fetch_replies(a, c))

        for a in PlayerEmpathyActivity.objects.select_related().all():
            update_list(a, getattr(a, 'empathy_answers'))

        for a in PlayerActivity.objects.select_related().all().order_by('type'):
            if a.type.type == 'open_ended':
                update_list(a, getattr(a, 'openended_answers'))
            elif a.type.type == 'single_response':
                update_list(a, getattr(a, 'singleresponse_answers'))

        for a in PlayerMapActivity.objects.select_related().all():
            update_list(a, getattr(a, 'map_answers'))

        for a in PlayerActivity.objects.select_related().filter(type__type='multi_response').order_by('mission'):
            answers = AnswerMultiChoice.objects.select_related().filter(option__activity=a)
            for answer in answers:
                for c in answer.comments.all():
                    mission_title = answer.option.mission.title
                    self.values_list.append(
                            (
                                c.pk, 
                                mission_title,
                                a.name,
                                'multichoice',
                                a.question,
                                c.posted_date.strftime('%Y-%m-%d %H:%M'),
                                c.user.pk,
                                answer.option.value,
                                c.message, 
                                c.likes.all().count(),
                            )
                    )
                    if c.comments.all().count():
                        self.values_list.extend(_fetch_multichoice_replies(answer, c, mission_title))

        super(ActivityReport, self).run(*args, **kwargs)

tasks.register(ActivityReport)
