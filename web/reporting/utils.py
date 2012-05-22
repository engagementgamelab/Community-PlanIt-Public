import xlwt
import StringIO
import os
from random import randint
from datetime import datetime, date

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import connection

from web.instances.models import Instance
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

class XslReport(object):

    def __init__(self, *args, **kwargs):
        self.debug = kwargs.pop('debug', settings.DEBUG)
        self.instance_id = kwargs.pop('instance_id')
        self.values_list = []
        self.field_titles = []
        self.notify_subject = None
        self.time_to_run = 0

        if self.instance_id is None:
            raise Exception("cannot run a report. No game provided")

    def run(self, *args, **kwargs):
        log.debug('running report for game id %s' % self.instance_id)
        log.debug('ran with %s queries' % len(connection.queries))
        filename = self.render_to_excel()
        log.debug('saved report to %s' %filename)

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

        report = Report.objects.create(
                title=self.notify_subject,
                instance=Instance.objects.get(pk=int(self.instance_id)),
                db_queries=len(connection.queries),
                time_to_run=self.time_to_run,
        )
        filename = "".join([self.notify_subject, "--", str(randint(1000, 10000)), '.xls'])
        location = os.path.join(settings.MEDIA_ROOT, determine_path(report, filename))
        new_dir = os.path.dirname(location)
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        output = StringIO.StringIO()
        xls.save(output)
        report.file.save(filename, ContentFile(output.getvalue()), save=True)
        output.close()
        log.debug('%s, saved %s' % (filename, location))
        return filename

