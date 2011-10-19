from datetime import datetime
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
from django.http import HttpResponseRedirect

def render_to_excel(values_list, field_titles, filename):
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
	pass

@login_required
def report_comments_popular(request):
	pass

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
            'points',
    )
    values_list = []
    users = UserProfile.objects.exclude(user__is_superuser=True, user__is_staff=True)
    for user in users:
        all_details = (
                user.pk,
                user.stake.stake if hasattr(user, 'stake') and user.stake is not None else "",
                user.race.race if hasattr(user, 'race') and user.race is not None else "",
                user.gender.gender if hasattr(user, 'gender') and user.gender is not None else "",
                user.education.education if hasattr(user, 'education') and user.education is not None else "",
                user.income.income if hasattr(user, 'income') and user.income is not None else "",
                user.living.situation if hasattr(user, 'living') and user.living is not None else "",
                ", ".join(user.affils.values_list('name', flat=True)) if hasattr(user, 'affils') else "",
                user.totalPoints,
        )
        values_list.append(all_details)
        #values_list.append((user.pk, 'comment1', '', '', '', ''))
        for c in user.user.comment_set.all():
            values_list.append((user.pk, c.message, '', '', '', ''))
    NOW = datetime.now()
    return render_to_excel(values_list, field_titles, NOW.strftime('%Y-%m-%d-%H-%M-'))

