import xlwt

import os
from random import randint
from datetime import datetime, date

from django.contrib.sites.models import Site
from django.db import connection
from django.core.mail import send_mail

from django.conf import settings
from django.db.models import Count

from web.instances.models import Instance

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

class Report(object):

    values_list = []
    field_titles = []
    notify_subject = None
    id = 0

    def run(self, *args, **kwargs):
        log.debug('ran with %s queries' % len(connection.queries))
        filename = self.render_to_excel()
        log.debug('saved report to %s' %filename)
        #self.notify_authors(filename)

    #def notify_authors(self, filename):
    #    subject = "report has been generated. %s" % self.notify_subject
    #    site = Site.objects.all()[0]
    #    url = "".join([site.domain, settings.MEDIA_ROOT, 'uploads/reports/',filename])
    #    body = "report available %s" % url
    #    send_mail(subject, body, settings.NOREPLY_EMAIL, settings.REPORTS_RECIPIENTS, fail_silently=False)

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
        game = Instance.objects.get(pk=self.instance_id)
        filename = "".join([game.slug, '-', self.notify_subject, '-', NOW.strftime('%Y-%m-%d-%H-%M'), 
                            "--", str(randint(1000, 10000)), '.xls'])
        location = os.path.join(settings.MEDIA_ROOT, 'uploads/reports', filename)
        xls.save(location)
        print '%s, saved %s' % (filename, location)
        return filename
