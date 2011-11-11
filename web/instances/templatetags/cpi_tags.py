import decimal
import logging
import os
import re
import types
import urllib
import urlparse

from django.conf import settings
from django.core.urlresolvers import reverse
from django import template
from django.utils.html import fix_ampersands
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _, get_language

from core.utils import get_translation_with_fallback

register = template.Library()

class PageNavigatorNode(template.Node):
    """
    Renders page navigation markup for a page of a django.core.paginator.Paginator.
    """
    def __init__(self, page, base_url, window_size=5, args=[]):
        self.page = page
        self.base_url = base_url
        self.window_size = window_size
        self.id_components = args
    
    def make_page_url(self, parsed_url, data):
        return urlparse.urlunparse((parsed_url[0], parsed_url[1], parsed_url[2], parsed_url[3], urllib.urlencode(data, True), parsed_url[5]))
    
    def render(self, context):
        page = template.Variable(self.page).resolve(context)
        url = template.Variable(self.base_url).resolve(context)
        parsed_url = urlparse.urlparse(url)
        data = urlparse.parse_qs(parsed_url[4])
        
        offset = 1 + self.window_size * ((page.number - 1) // self.window_size)
        last_page = min(page.paginator.num_pages + 1, offset + self.window_size)

        li_template = '<li class="%s">%s</li>'
        link_template = '<a href="%s">%s</a>'

        output = ''

        # support multiple paginators per template
        page_param = 'page'
        for component in self.id_components:
            page_param += '_%s' % template.Variable(component).resolve(context)

        if page.paginator.num_pages > 0:
            output = '<ul class="page_navigator">'
            if page.has_previous():
                data[page_param] = page.previous_page_number()
                link = link_template % (self.make_page_url(parsed_url, data), '<img src="%simg/icons/paginator_previous.png" alt="previous"/>' % settings.MEDIA_URL)
                output += li_template % ('prev', link) 

            for i in range(offset, last_page):
                link = i
                if page.number != i:
                    data[page_param] = i
                    link = link_template % (self.make_page_url(parsed_url, data), i)
                output += li_template % ('current %s' % (i == last_page - 1 and ' final' or ''), link)

            if page.has_next():
                data[page_param] = page.next_page_number()
                link = link_template % (self.make_page_url(parsed_url, data), '<img src="%simg/icons/paginator_next.png" alt="next"/>' % settings.MEDIA_URL)
                output += li_template % ('next', link) 

            output += "</ul>"
        return mark_safe(fix_ampersands(output))

@register.tag
def pagenavigator(parser, argument_string):
    """

    The pagenavigator tag requires a Paginator.Page object and a base URL.

    The optional third argument is the number of pages to create links for.
    Think of this as the size of the window you can slide through the
    paginator's pages.

    Any additional arguments are used to qualify the page number in the query
    parameters of the page links; this allows you to create multiple paginators
    per template.

    """

    argv = argument_string.split_contents()
    argc = len(argv)
    if argc == 3:
        return PageNavigatorNode(argv[1], argv[2])
    elif argc == 4:
        return PageNavigatorNode(argv[1], argv[2], argv[3])
    elif argc > 4:
        return PageNavigatorNode(argv[1], argv[2], argv[3], argv[4:])
    
    raise template.TemplateSyntaxError('The %s tag requires a paginator page and a base URL.' % argv[0])


@register.filter
def teaser(text, word_count):
    teaser = ' '.join(text.split()[:word_count])
    last_dot = teaser.rfind('.') + 1
    teaser = teaser[:last_dot]
    if len(teaser) < len(text):
        teaser += '...'
    return teaser

@register.filter
def trans_fallback(obj, attr):
	return get_translation_with_fallback(obj, attr)

@register.filter
def order_by(queryset, args):
    print "order_by", args
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)

@register.filter
def order_by_custom(queryset):
    print "order_by_custom"
    #import ipdb;ipdb.set_trace()
    return queryset.order_by(*args)


@register.simple_tag(takes_context=True)
def format_action(context):
    """ 
        Admin created a response to [activity or challenge name].  

        If it's a challenge, the full news item should say: 
            "Admin created a response to [challenge name] created by [user name].
    """
    action = context.get('action')
    if not action:
        return ""

    if not action.actor.is_superuser:
        actor_format = '<a href="%s">%s</a>' %(reverse('accounts_profile', args=(action.actor.pk,)), action.actor.get_profile().screen_name)
    else:
        actor_format = 'Admin'

    if action.action_object:
        obj = action.action_object
        klass = obj.__class__.__name__
        if  klass in \
                        ['PlayerActivityOfficialResponse', 
                         'MapOfficialResponse', 
                         'EmpathyOfficialResponse',
                        ]:

            target_url = '<a href="%s">%s</a>' % (obj.activity.get_absolute_url(), 
                                                  obj.activity.stream_action_title)

            return "%s %s to %s" % ( actor_format,
                                     action.get_verb_display(),
                                     target_url,
            )

        elif klass in ['ChallengeOfficialResponse',]:
            challenge_creator = '<a href="%s">%s</a>' %( reverse('accounts_profile', args=(obj.challenge.user.pk,)),
                                                         obj.challenge.user.get_profile().screen_name)
            target_url = '<a href="%s">%s</a>' % (obj.get_absolute_url(),
                                                  obj.stream_action_title)
            return "%s %s %s created by %s" % ( actor_format, 
                                                action.get_verb_display(), 
                                                target_url,
                                                challenge_creator,
            )

        if obj.__class__.__name__ in \
                                    ['Challenge', ]:
            target_url = '<a href="%s">%s</a>' % (obj.get_absolute_url(), 
                                                  obj.stream_action_title)
            return "%s %s %s" % ( actor_format, 
                                     action.get_verb_display(), 
                                     target_url,
            )

    return ""
