from stream.models import Action

from web.accounts.models import UserProfilePerInstance, UserProfile
from web.answers.models import AnswerMultiChoice
from web.badges.models import BadgePerPlayer
from web.missions.models import Mission
from .utils import Report


def get_demographic_field_titles():
    return (
            'ID', 
            'first name',
            'last name',
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
    )

def get_demographic_details(user_prof_per_instance, profile, user, instance_id):

    def get_stakes(profile):
        return profile.format_stakes

    def get_affiliations(profile):
        return ", ".join(profile.affils.values_list('name', flat=True))

    return (
        user_prof_per_instance.pk,
        user.first_name,
        user.last_name,
        get_stakes(user_prof_per_instance),
        get_affiliations(user_prof_per_instance),
        user_prof_per_instance.preferred_language.name,
        "Yes" if profile.avatar else "No",
        profile.race.race if hasattr(profile, 'race') and profile.race is not None else "",
        profile.gender.gender if hasattr(profile, 'gender') and profile.gender is not None else "",
        profile.education.education if hasattr(profile, 'education') and profile.education is not None else "",
        profile.income.income if hasattr(profile, 'income') and profile.income is not None else "",
        profile.living.situation if hasattr(profile, 'living') and profile.living is not None else "",
        profile.city or "",
        profile.zip_code or "",
    )

class DemographicReport(Report):
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

    def run(self, *args, **kwargs):
        self.instance_id = kwargs.get('instance_id')
        self.notify_subject = "Demographic-Report"


        self.field_titles = get_demographic_field_titles() + (
                'number of log-ins',
                'total flags spent for game', 
                'total points for game', 
                'badges earned', 
                'challenge completed count',
                'challenges created count',
                'comments liked count',
                'comments replied to count',
        )
        self.values_list = []

        for user_prof_per_instance in UserProfilePerInstance.objects.filter(
                                                    instance__id=self.instance_id).\
                                                exclude(
                                                    user_profile__user__is_superuser=True,
                                                    user_profile__user__is_staff=True,):

            profile =  user_prof_per_instance.user_profile
            user =  user_prof_per_instance.user_profile.user
            all_details = get_demographic_details(user_prof_per_instance, profile, user, self.instance_id) + (
                    Action.objects.get_for_actor(user).filter(verb='user_logged_in').count(),
                    user_prof_per_instance.flags,
                    user_prof_per_instance.total_points,
                    ", ".join(BadgePerPlayer.objects.filter(user=user).values_list('badge__title', flat=True)),
                    Action.objects.get_for_actor(user).filter(verb='activity_completed', target_instance__pk=self.instance_id).count(),
                    Action.objects.get_for_actor(user).filter(verb='activity_player_submitted', target_instance__pk=self.instance_id).count(),
                    Action.objects.get_for_actor(user).filter(verb='liked', target_comment__instance__pk=self.instance_id).count(),
                    Action.objects.get_for_actor(user).filter(verb='commented', target_comment__instance__pk=self.instance_id).count(),
            )
            self.values_list.append(all_details)
        super(DemographicReport, self).run(*args, **kwargs)


class LoginActivityReport(Report):
    """
        -- activity time by user - 
        this report should include user name and demographic data and when they logged in.  """


    def run(self, *args, **kwargs):
        self.instance_id = kwargs.get('instance_id')
        self.notify_subject = "Login-Activity-Report"


        self.field_titles = get_demographic_field_titles() + (
                'number of log-ins',
                'login dates/times',
        )
        self.values_list = []

        for user_prof_per_instance in UserProfilePerInstance.objects.filter(
                                                    instance__id=self.instance_id).\
                                                exclude(
                                                    user_profile__user__is_superuser=True,
                                                    user_profile__user__is_staff=True,):

            profile =  user_prof_per_instance.user_profile
            user =  user_prof_per_instance.user_profile.user


            login_actions = Action.objects.get_for_actor(user).filter(verb='user_logged_in')

            datetimes = login_actions.values_list('datetime', flat=True)

            all_details = get_demographic_details(user_prof_per_instance, profile, user, self.instance_id) + (
                    login_actions.count(),
                    ", ".join([dt.strftime('%Y-%m-%d-%H-%M') for dt in datetimes]),
            )
            self.values_list.append(all_details)
        super(LoginActivityReport, self).run(*args, **kwargs)



def fetch_replies(answer, comment, pad_columns=None):
    replies = []
    if pad_columns == None:
        pad_columns=('-','-','-','-','-','-','-','-','-','-','-','-','-','-',)
    else:
        pad_columns = ()
    if comment.comments.all().count():
        for res in comment.comments.select_related().all():
            replies.append(
                pad_columns+ (
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
            #fetch_replies(a, res)
    return replies

def _fetch_multichoice_replies(answer, comment, mission_title, pad_columns=None):
    if pad_columns == None:
        pad_columns=('-','-','-','-','-','-','-','-','-','-','-','-','-','-',)
    else:
        pad_columns = ()
    replies = []
    for res in comment.comments.all():
        replies.append(
                pad_columns+ (
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
        #_fetch_multichoice_replies(a, res, mission_title=mission_title)
    return replies

def update_list(values_list, user=None, activity=None, answers=None, pad_columns=None):
    if pad_columns == None:
        pad_columns=('-','-','-','-','-','-','-','-','-','-','-','-','-','-',)
    else:
        pad_columns = ()
    if answers is None:
        return
    answers = answers.select_related('comments')
    if user is not None:
        answers = answers.filter(answerUser=user)
    for answ in answers:
        for c in answ.comments.select_related('user', 'selected', 'likes').all():
            if activity.type.type == 'single_response':
                answer_value = answ.selected.value
            else:
                answer_value = ''

            values_list.append(
                    pad_columns +
                    (
                        c.pk, 
                        activity.mission.title,
                        activity.name, 
                        activity.type.type, 
                        activity.question,
                        c.posted_date.strftime('%Y-%m-%d %H:%M'),
                        c.user.get_profile().screen_name,
                        answer_value,
                        c.message, 
                        c.likes.all().count(),
                    )
            )
            if c.comments.all().count():
                values_list.extend(fetch_replies(activity, c))



class ChallengeActivityReport(Report):
    """
        -- record of challenge activity by user - this report should include user name and demographic data and their record of all challenge activity. 
        This should include responses to challenges (if multiple choice) and comments. """

    def run(self, *args, **kwargs):
        self.instance_id = kwargs.get('instance_id')
        self.notify_subject = "Challenge-Activity-Report"

        self.field_titles = get_demographic_field_titles() + (
                            'comment id', 
                            'mission', 
                            'activity title', 
                            'challenge type', 
                            'original question',
                            'timestamp',
                            'user id',
                            'response code',
                            'comment', 
                            'likes'
        )
        self.values_list = []


        for user_prof_per_instance in UserProfilePerInstance.objects.filter(
                                                    instance__id=self.instance_id).\
                                                exclude(
                                                    user_profile__user__is_superuser=True,
                                                    user_profile__user__is_staff=True):
            profile =  user_prof_per_instance.user_profile
            user =  user_prof_per_instance.user_profile.user

            demographic_details = get_demographic_details(user_prof_per_instance, profile, user, self.instance_id)
            self.values_list.append(demographic_details)

            actions = Action.objects.get_for_actor(user).filter(verb='activity_completed')
            for action in actions:
                obj = action.action_object
                if obj.__class__.__name__ ==  'PlayerEmpathyActivity':
                    update_list(self.values_list, user, obj, getattr(obj, 'empathy_answers'))
                if obj.__class__.__name__ ==  'PlayerActivity':
                    if obj.type.type == 'open_ended':
                        update_list(self.values_list, user, obj, getattr(obj, 'openended_answers'))
                    if obj.type.type == 'single_response':
                        update_list(self.values_list, user, obj, getattr(obj, 'singleresponse_answers'))
                    if obj.type.type == 'multi_response':
                        answers = AnswerMultiChoice.objects.select_related().filter(option__activity=obj)
                        for answer in answers:
                            for c in answer.comments.filter(user=user):
                                mission_title = answer.option.mission.title
                                self.values_list.append(
                                        (
                                            '-','-','-','-','-','-','-','-','-','-','-','-','-','-',
                                            c.pk, 
                                            mission_title,
                                            obj.name,
                                            'multichoice',
                                            obj.question,
                                            c.posted_date.strftime('%Y-%m-%d %H:%M'),
                                            c.user.pk,
                                            answer.option.value,
                                            c.message, 
                                            c.likes.all().count(),
                                        )
                                )
                                if c.comments.all().count():
                                    self.values_list.extend(_fetch_multichoice_replies(answer, c, mission_title))
                if obj.__class__.__name__ == 'PlayerMapActivity':
                    update_list(obj, getattr(obj, 'map_answers'))

        super(ChallengeActivityReport, self).run(*args, **kwargs)



class MissionReport(Report):

    """-- mission report - 
        organized by challenge; 
        if multiple choice (summary of results); 
        and all comments and replies."""

    def run(self, *args, **kwargs):
        self.instance_id = kwargs.get('instance_id')
        self.notify_subject = "Mission-Report"

        self.field_titles = (
                            'mission', 
                            'comment id', 
                            'activity title', 
                            'activity type', 
                            'original question',
                            'timestamp',
                            'user id',
                            'response code',
                            'comment', 
                            'likes'
        )
        self.values_list = []
        for mission in Mission.objects.filter(instance__pk=self.instance_id):
            for obj in mission.get_activities(include_player_submitted=True):
                if obj.__class__.__name__ ==  'PlayerEmpathyActivity':
                    update_list(self.values_list, user=None, activity=obj, answers=getattr(obj, 'empathy_answers'))
                if obj.__class__.__name__ ==  'PlayerActivity':
                    if obj.type.type == 'open_ended':
                        update_list(self.values_list, user=None, activity=obj, answers=getattr(obj, 'openended_answers'))
                    if obj.type.type == 'single_response':
                        update_list(self.values_list, user=None, activity=obj, answers=getattr(obj, 'singleresponse_answers'))
                    if obj.type.type == 'multi_response':
                        answers = AnswerMultiChoice.objects.select_related().filter(option__activity=obj)
                        for answer in answers:
                            for c in answer.comments.all():
                                #mission_title = answer.option.mission.title
                                mission_title = mission.title
                                self.values_list.append(
                                        (
                                            mission_title,
                                            c.pk, 
                                            obj.name,
                                            'multichoice',
                                            obj.question,
                                            c.posted_date.strftime('%Y-%m-%d %H:%M'),
                                            c.user.pk,
                                            answer.option.value,
                                            c.message, 
                                            c.likes.all().count(),
                                        )
                                )
                                if c.comments.all().count():
                                    self.values_list.extend(_fetch_multichoice_replies(answer, c, mission_title))
                if obj.__class__.__name__ == 'PlayerMapActivity':
                    update_list(obj, getattr(obj, 'map_answers'))

        super(MissionReport, self).run(*args, **kwargs)
