from datetime import datetime
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from accounts.models import UserProfile
from comments.models import Comment
from answers.models import AnswerMultiChoice

#from player_activity.models import *

def render_to_excel(values_list, field_titles=[], filename='report'):
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
    from player_activities.models import PlayerEmpathyActivity, PlayerMapActivity, PlayerActivity
    #empathy_comments = Comment.objects.filter(content_type__model='playerempathyactivity').order_by('user__pk').values_list('user__pk', 'message')

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
def report_comments_popular(request):
    values_list = Comment.objects.annotate(num_likes=Count('likes')).filter(num_likes__gt=2).values_list('user__pk', 'num_likes', 'message').order_by('user__pk')
    NOW = datetime.now()
    return render_to_excel(values_list, field_titles=('user id', 'num of likes', 'message'), filename=NOW.strftime('%Y-%m-%d-%H-%M-popular_comments'))

@login_required
def report_general(request):
    """
    - race/ethnicity
    - income
    - gender
    - stake
    - affiliations
    - points
    - token distribution
    - date of birth
    - city
    - zip_code
    """
    field_titles = (
            'ID',
            'stake',
            'race',
            'gender',
            'education',
            'income',
            'living',
            'affiliations',
            'birth year',
            'city/neighborhood',
            'zip code',
            'how discovered?',
            'points',
    )
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

