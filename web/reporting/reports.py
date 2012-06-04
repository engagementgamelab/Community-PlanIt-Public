import os
import xlwt
import time
from stream.models import Action
import StringIO
from random import randint
from datetime import datetime, date
from operator import attrgetter

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import connection

from web.accounts.models import UserProfilePerInstance, UserProfile
from web.answers.models import AnswerMultiChoice
from web.badges.models import BadgePerPlayer
from web.instances.models import Instance
from web.missions.models import Mission
from .models import Report, determine_path

import logging
log = logging.getLogger()


"""
BEHOLD! The Spec!

Reports:

-- activity report by user - this report should be organized by user name and include all demographic data, number of log-ins, flag placement, badges earned, number of challenges completed, number of challenges created, number of comments liked, number of comments replied to.

-- activity time by user - this report should include user name and demographic data and when they logged in.

-- record of challenge activity by user - this report should include user name and demographic data and their record of all challenge activity. This should include responses to challenges (if multiple choice) and comments.

-- mission report - organized by challenge; if multiple choice (summary of results); and all comments and replies.

all registration data, points, badges, and flag placements, should be included in all reports organized by user.
"""

#class ReportProxy(object):
#    def __init__(self, report):
#        self.__report = report
#    def __getattr__(self, name):
#        return getattr(self.__report, name)


def get_report_instance(report_label):
    """ find the report class for the named report """
    try:
        report_name = settings.CPI_REPORTS[report_label]
    except (KeyError, AttributeError):
        raise ImproperlyConfigured("settings.CPI_REPORTS is not configured correctly for %r" % report)

    # 'report_label' : ('app.module','ReportClass')
    # from app.module load ReportClass and instantiate
    report_module = __import__( report_name[0],{},{},[''])
    report_class = getattr(report_module,report_name[1] )
    return report_class


class ReportData(object):

    def __init__(self, **kwargs):
        self.field_titles = kwargs.pop('field_titles')
        self.values_list = kwargs.pop('values_list')
        self.exec_time = kwargs.pop('exec_time')
        self.query_count = kwargs.pop('query_count')


class ReportHandler(object):

    def __init__(self, *args, **kwargs):
        self.game_id = kwargs.pop('game_id')
        self.debug = False

    def run_reports(self):

        if self.game_id is not None:
            games = Instance.objects.filter(pk=self.game_id)
        else:
            games = Instance.objects.current()

        for report_label in settings.CPI_REPORTS.keys():

            for game in games:
                xls_report = XlsReport()
                report_instance = get_report_instance(report_label)(game, debug=self.debug)
                if report_instance.__class__.__name__  == 'MissionReport':
                    for mission in game.missions.all():
                        data = report_instance.get_report_data(game, [mission,])
                        sheet = xls_report.wb.add_sheet(mission.title)
                        xls_report.write_titles(sheet, data.field_titles)
                        xls_report.write_data(sheet, data.values_list)
                else:
                    data = report_instance.get_report_data(game)
                    sheet = xls_report.wb.add_sheet(report_instance.__class__.__name__)
                    xls_report.write_titles(sheet, data.field_titles)
                    xls_report.write_data(sheet, data.values_list)

                output = xls_report.render_to_excel()

                title = "".join([game.slug, '-', report_label])
                report = Report.objects.create(
                        title=title,
                        instance=game,
                        db_queries=data.query_count,
                        exec_time=data.exec_time,
                )
                NOW = datetime.now()
                filename = "".join([NOW.strftime('%Y-%m-%d-%H-%M'), '-', title, '.xls'])
                location = os.path.join(settings.MEDIA_ROOT, determine_path(report, filename))
                new_dir = os.path.dirname(location)
                if not os.path.exists(new_dir):
                    os.mkdir(new_dir)

                report.file.save(filename, ContentFile(output.getvalue()), save=True)
                output.close()
                log.debug('done with report. %s, saved %s' % (filename, location))
                del report_instance 


class XlsReport(object):

    def __init__(self):
        #self.report_title = data.report_title
        #self.values_list = data.values_list
        #self.field_titles = data.field_titles

        self.wb = xlwt.Workbook(encoding='utf8')
        self.default_style = xlwt.Style.default_style

        self.header_style =xlwt.XFStyle()
        header_background = xlwt.Pattern()
        header_background.pattern = xlwt.Pattern.SOLID_PATTERN
        header_background.pattern_fore_colour = 22

        header_font = xlwt.Font()
        header_font.name = 'Calibri'
        header_font.bold = True
        self.header_style.pattern = header_background

    def write_titles(self, sheet, field_titles):
        for col, val in enumerate(field_titles):
            sheet.write(0, col, val, style=self.header_style)

    def write_data(self, sheet, values_list):
        datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
        date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')

        for row, rowdata in enumerate(values_list, start=1):
            for col, val in enumerate(rowdata):
                if isinstance(val, datetime):
                    style = datetime_style
                elif isinstance(val, date):
                    style = date_style
                else:
                    style = self.default_style
                sheet.write(row, col, val, style=style)

        #if not save_to_file:
        #    return xls_to_response(wb, filename)

    def render_to_excel(self, save_to_file=True):
        output = StringIO.StringIO()
        self.wb.save(output)
        return output


class DemographicReport(object):
    """ -- activity report by user - 
        this report should be organized by user name and 
        - include 
            all demographic data, 
            number of log-ins, 
            flag placement, 
            badges earned, 
            number of challenges completed, 
            number of challenges created, 
            number of comments liked, 
            number of comments replied to.  """

    def __init__(self, game, qs=None, debug=True):
        self.debug = debug

        if not qs:
            self.qs = UserProfilePerInstance.objects.filter(
                                            instance=game).\
                                        exclude(
                                            user_profile__user__is_superuser=True,
                                            user_profile__user__is_staff=True,
                                            )
        if self.debug:
            self.qs = self.qs.filter(user_profile__user__pk=877)

    def get_demographic_field_titles(self):
        return (
                'ID', 
                'first name',
                'last name',
                'email',
                'stake', 
                'affiliations', 
                'preferred language', 
                'picture', 
                'race', 
                'gender', 
                'education', 
                'income', 
                'rent/own', 
                'city/neighborhood', 
                'zip code', 
                'birth_year',
                'how discovered',
                'how discovered (other)',
        )

    def get_demographic_details(self, prof_per_instance, profile, user):

        def get_stakes(profile):
            return profile.format_stakes

        def get_affiliations(profile):
            return ", ".join(profile.affils.values_list('name', flat=True))

        return (
            prof_per_instance.pk,
            user.first_name,
            user.last_name,
            profile.email,
            get_stakes(prof_per_instance),
            get_affiliations(prof_per_instance),
            prof_per_instance.preferred_language.name,
            "Yes" if profile.avatar else "No",
            profile.race.race if hasattr(profile, 'race') and profile.race is not None else "",
            profile.gender.gender if hasattr(profile, 'gender') and profile.gender is not None else "",
            profile.education.education if hasattr(profile, 'education') and profile.education is not None else "",
            profile.income.income if hasattr(profile, 'income') and profile.income is not None else "",
            profile.living.situation if hasattr(profile, 'living') and profile.living is not None else "",
            profile.city or "",
            profile.zip_code or "",
            profile.birth_year or "",
            profile.how_discovered.how if hasattr(profile, 'how_discovered') and profile.how_discovered is not None else "",
            profile.how_discovered_other or "",
        )

    def get_report_data(self, game):

        field_titles = self.get_demographic_field_titles() + (
                'number of log-ins',
                'total flags spent for game', 
                'total points for game', 
                'badges earned', 
                'challenge completed count',
                'challenges created count',
                'comments liked count',
                'comments replied to count',
        )

        t1 = time.time()
        values_list = []
        for prof_per_instance in self.qs:

            profile =  prof_per_instance.user_profile
            user =  prof_per_instance.user_profile.user
            all_details = self.get_demographic_details(prof_per_instance, profile, user) + (
                    Action.objects.get_for_actor(user).filter(
                                                        verb='user_logged_in',
                                                        target_instance=game,
                        ).count(),
                    prof_per_instance.flags,
                    prof_per_instance.total_points,
                    ", ".join(BadgePerPlayer.objects.filter(user=user).values_list('badge__title', flat=True)),
                    Action.objects.get_for_actor(user).filter(
                                                        verb='activity_completed', 
                                                        target_instance=game
                        ).count(),
                    Action.objects.get_for_actor(user).filter(
                                                        verb='activity_player_submitted', 
                                                        target_instance=game
                        ).count(),
                    Action.objects.get_for_actor(user).filter(
                                                        verb='liked', 
                                                        target_comment__instance=game
                        ).count(),
                    Action.objects.get_for_actor(user).filter(
                                                        verb='commented', 
                                                        target_comment__instance=game
                        ).count(),
            )
            values_list.append(all_details)

        return ReportData(
                field_titles = field_titles,
                values_list = values_list,
                exec_time = time.time()-t1,
                query_count = len(connection.queries),
        )


class LoginActivityReport(DemographicReport):
    """
        -- activity time by user - 
        this report should include user name and demographic data and when they logged in.  """


    def get_report_data(self, game):

        field_titles = self.get_demographic_field_titles() + (
                #'number of log-ins',
                'login dates/times',
        )
        t1 = time.time()
        values_list = []
        for prof_per_instance in self.qs:

            profile =  prof_per_instance.user_profile
            user =  prof_per_instance.user_profile.user

            demographic_details = self.get_demographic_details(prof_per_instance, profile, user)
            login_actions = Action.objects.get_for_actor(user).filter(
                                        verb='user_logged_in',
                                        target_instance=game,
                            )
            datetimes = login_actions.values_list('datetime', flat=True)

            for dt in datetimes:
                all_details =  demographic_details+ (
                        #login_actions.count(),
                        dt.strftime('%Y-%m-%d-%H-%M'),
                )
                values_list.append(all_details)

        return ReportData(
                field_titles = field_titles,
                values_list = values_list,
                exec_time = time.time()-t1,
                query_count = len(connection.queries),
        )


class ChallengeActivityReport(DemographicReport):
    """
        -- record of challenge activity by user 
        - this report should include user name and demographic data and their record of all challenge activity. 
        This should include responses to challenges (if multiple choice) and comments. """

    def get_report_data(self, game, missions=[]):
        values_list = []
        t1 = time.time()
        def _gen_answer_classes():
            answer_classes = {}
            _module = __import__('web.answers.models',{},{},[''])
            for ans_class, ch_class in (
                    ('AnswerSingleResponse', 'PlayerActivity_single_response'),
                    ('AnswerMap', 'PlayerMapActivity_map'),
                    ('AnswerEmpathy',  'PlayerEmpathyActivity_empathy'),
                    ('AnswerOpenEnded', 'PlayerActivity_open_ended')):
                answer_classes[ch_class] = getattr(_module, ans_class)
            return answer_classes
        _answer_classes = _gen_answer_classes()
        players = self.qs

        if len(missions) == 0:
            missions = Mission.objects.for_instance(game)

        activities = []
        for mission in missions:
            activities.extend(mission.activities)
            log.debug("mission %s, activities count: %s" % (mission.title, len(activities)))
        activities = sorted(activities, key=attrgetter('mission', 'type'))

        players_count = players.count()

        for i, prof_per_instance in enumerate(players):
            profile =  prof_per_instance.user_profile
            user =  prof_per_instance.user_profile.user
            row = ()
            completed_cnt = 0
            demographic_details = self.get_demographic_details(prof_per_instance, profile, user)

            for activity in activities:
                actions = Action.objects.get_for_action_object(activity).filter(verb='activity_completed', actor_user=user)
                #print "got actions %s for user %s" % (actions, user)
                if actions.count() == 0:
                    continue
                else:
                    completed_cnt += 1
                    activity = actions[0].action_object
                    obj_pk = activity.pk
                    obj_class_name = activity.__class__.__name__
                    obj_type = activity.activity_type_readable
                    if obj_type == 'multi_response':
                        my_answers_as_str = AnswerMultiChoice.objects.my_answers_by_activity_as_str(
                                                        activity, user,
                        )
                        my_answers_likes_count = AnswerMultiChoice.objects.my_answers_by_activity_likes_count(
                                                        activity, user
                        )
                        answer_class = AnswerMultiChoice
                    else:
                        answer_class = _answer_classes.get(obj_class_name+'_'+obj_type)
                        my_answers_as_str = answer_class.objects.my_answers_by_activity_as_str(activity, user)
                        my_answers_likes_count = answer_class.objects.my_answers_by_activity_likes_count(activity, user)
                    answers  = answer_class.objects.my_answers_by_activity(activity, user)

                    for answ in answers:
                        for c in answ.comments.select_related('user', 'selected', 'likes').all():
                            activity_formatted = activity.name + ' - ' + obj_type
                            activity_question = activity.question
                            comments_list = (
                                activity_formatted,
                                activity_question,
                                my_answers_as_str,
                                c.pk,
                                c.posted_date.strftime('%Y-%m-%d %H:%M'),
                                c.message,
                                '-',
                                my_answers_likes_count,
                            )
                            values_list.append(demographic_details + comments_list)
                            for reply in c.comments.all():

                                prof_per_instance = UserProfilePerInstance.objects.get(
                                                                instance=game,
                                                                user_profile__user=reply.user,
                                )
                                reply_demographic_details = self.get_demographic_details(prof_per_instance, prof_per_instance.user_profile, reply.user)
                                reply_list = (
                                    '', '', 
                                    'In response to #%s' % c.pk,
                                    reply.pk,
                                    reply.posted_date.strftime('%Y-%m-%d %H:%M'),
                                    '',
                                    reply.message,
                                    my_answers_likes_count,
                                )
                                values_list.append(reply_demographic_details + reply_list)
            #if completed_cnt > 0:
            #    print "%s of %s. %s competed %s challenges" % (i, players_count, profile.screen_name, completed_cnt)
        field_titles = self.get_demographic_field_titles() + (
            'challenge title/type',
            'original question',
            'response',
            'comment id',
            'timestamp',
            '_ddqual_comment',
            '_ddqual_reply',
            'likes count',
        )
        log.debug("report done in %s min. %s queries." % ((time.time()-t1)/60, len(connection.queries)))
        return ReportData(
                field_titles = field_titles,
                values_list = values_list,
                exec_time = time.time()-t1,
                query_count = len(connection.queries),
        )


class MissionReport(DemographicReport):

    def get_report_data(self, game, missions=[]):
        values_list = []
        t1 = time.time()
        field_titles = self.get_demographic_field_titles()

        def _gen_answer_classes():
            answer_classes = {}
            _module = __import__('web.answers.models',{},{},[''])
            for ans_class, ch_class in (
                    ('AnswerSingleResponse', 'PlayerActivity_single_response'),
                    ('AnswerMap', 'PlayerMapActivity_map'),
                    ('AnswerEmpathy',  'PlayerEmpathyActivity_empathy'),
                    ('AnswerOpenEnded', 'PlayerActivity_open_ended')):
                answer_classes[ch_class] = getattr(_module, ans_class)
            return answer_classes
        _answer_classes = _gen_answer_classes()
        players = self.qs

        if len(missions) == 0:
            missions = Mission.objects.for_instance(game)

        activities = []
        for mission in missions:
            activities.extend(mission.activities)
            print "mission %s, activities count: %s" % (mission.title, len(activities))
        activities = sorted(activities, key=attrgetter('mission', 'type'))

        players_count = players.count()
        for obj in activities:
            obj_pk = obj.pk
            field_titles += (
                    'challenge title/type %s' % obj_pk,
                    'original question %s' % obj_pk,
                    '_ddqual_response %s' % obj_pk,
                    'likes %s' % obj_pk,
            )
        for i, prof_per_instance in enumerate(players):
            profile =  prof_per_instance.user_profile
            user =  prof_per_instance.user_profile.user
            demographic_details = self.get_demographic_details(prof_per_instance, profile, user)

            row = demographic_details
            completed_cnt = 0

            for activity in activities:
                actions = Action.objects.get_for_action_object(activity).filter(actor_user=user)
                #print "got actions %s for user %s" % (actions, user)
                if actions.count() == 0:
                    this_activity = ('', '', '', '')
                else:
                    completed_cnt += 1
                    obj = actions[0].action_object
                    obj_pk = obj.pk
                    obj_class_name = obj.__class__.__name__
                    obj_type = obj.activity_type_readable
                    if obj_type == 'multi_response':
                        my_answers_as_str = AnswerMultiChoice.objects.my_answers_by_activity_as_str(
                                                        obj, user,
                        )
                        my_answers_likes_count = AnswerMultiChoice.objects.my_answers_by_activity_likes_count(
                                                        obj, user
                        )
                    else:
                        answer_class = _answer_classes.get(obj_class_name+'_'+obj_type)
                        my_answers_as_str = answer_class.objects.my_answers_by_activity_as_str(obj, user)
                        my_answers_likes_count = answer_class.objects.my_answers_by_activity_likes_count(obj, user)

                    this_activity = (
                        obj.name + ' - ' + obj_type,
                        obj.question,
                        my_answers_as_str,
                        my_answers_likes_count,
                    )
                row += this_activity
            if completed_cnt > 0:
                print "%s of %s. %s competed %s challenges" % (i, players_count, profile.screen_name, completed_cnt)
                values_list.append(row)
        print "done in %s min. %s queries." % ((time.time()-t1)/60, len(connection.queries))
        return ReportData(
                field_titles = field_titles,
                values_list = values_list,
                exec_time = time.time()-t1,
                query_count = len(connection.queries),
        )

