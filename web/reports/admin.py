from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.menu import items, Menu
from admin_tools.utils import get_admin_site_name

from reports.models import *

admin.site.register(Activity)


class ReportsMenu(Menu):
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children += [
            items.MenuItem('Home', reverse('admin:index')),
            items.MenuItem(_('Dashboard'), reverse('%s:index' % site_name)),
            items.Bookmarks(),
            items.AppList(
                _('Applications'),
                exclude=('django.contrib.*',)
            ),
            items.AppList(
                _('Administration'),
                models=('django.contrib.*',)
            ),
            items.MenuItem('Excel Reports',
                children=[
                    items.MenuItem('general', reverse('reports:general')),
                    items.MenuItem('popular comments', reverse('reports:comments_popular')),
                    items.MenuItem('comments by activity', reverse('reports:comments_by_activity')),
                ]
            ),
        ]
