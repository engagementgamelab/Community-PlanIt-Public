from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.menu import items, Menu
from admin_tools.utils import get_admin_site_name

from web.instances.models import Instance, City


class ReportsMenu(Menu):
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        city_menu_items = []
        for city in City.objects.all().order_by('name'):
            game_menu_items = []
            for game in Instance.objects.filter(for_city=city).order_by('title'):
                available_reports =  [
                    {
                        'name': 'demographic', 
                        'url': reverse('reporting:run-report', args=('demographic', game.pk,)),
                    },
                ]
                reports_menu_items = []
                for report_data in available_reports:
                    reports_menu_items.append(
                        items.MenuItem('%s' % report_data['name'], report_data['url'])
                    )
                game_menu_items.append(
                        items.MenuItem('%s' % game.title, children=reports_menu_items)
                )

            city_menu_items.append(
                    items.MenuItem('%s' % city.name, children=game_menu_items)
            )

        self.children += [
            items.MenuItem('Home', reverse('admin:index')),
            items.MenuItem(_('Dashboard'), reverse('%s:index' % site_name)),
            #items.Bookmarks(),
            items.MenuItem('Excel Reports',
                children = city_menu_items
            ),
            items.AppList(
                _('Applications'),
                exclude=('django.contrib.*',)
            ),
            items.AppList(
                _('Administration'),
                models=('django.contrib.*',)
            ),
        ]
