import decimal
import logging
import os
import re
import types
import urllib
import urlparse

from django.conf import settings
from django import template
from django.template.defaultfilters import stringfilter
from django.utils import simplejson
from django.utils.encoding import force_unicode
from django.utils.functional import Promise
from django.utils.html import fix_ampersands
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _, get_language

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
def trans_fallback(obj, attr):
    if not get_language() in obj.get_available_languages():
        return getattr(obj.translations.get(language_code=settings.LANGUAGE_CODE), attr)
    return getattr(obj, attr)

@register.filter
def teaser(text, word_count):
    teaser = ' '.join(text.split()[:word_count])
    last_dot = teaser.rfind('.') + 1
    teaser = teaser[:last_dot]
    if len(teaser) < len(text):
        teaser += '...'
    return teaser

