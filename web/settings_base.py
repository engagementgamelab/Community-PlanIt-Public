# -- coding: utf-8 --
import os
import sys
import re
import logging

ROOTDIR = os.path.dirname(os.path.realpath(__file__))

#
# Standard Django settings
#
ADMIN_MEDIA_PREFIX = '/admin-media/'

#admin_tools
ADMIN_TOOLS_MEDIA_URL = '/static/'
ADMIN_TOOLS_MENU = 'web.reports.admin.ReportsMenu'

ADMINS = ( ('Benedict Holland', 'sheepskin505@gmail.com'), )
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
AUTHENTICATION_BACKENDS = ( 'web.accounts.backends.EmailBackend', )
DATE_FORMAT = '%m/%d/%Y'
DEBUG = False
DEFAULT_FROM_EMAIL = 'noreply@communityplanit.org'
DIRNAME = os.path.dirname(__file__)

INTERNAL_IPS = ('127.0.0.1',)

# DATABASES: complete your database configuration in settings.py

EMAIL_BACKEND = 'django_mailer.smtp_queue.EmailBackend'

INSTALLED_APPS = (
    # localeurl should be first
    'localeurl',   
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',

    'web',
    'web.accounts',
    'web.answers',
    'web.attachments',
    'web.challenges',
    'web.comments',
    'web.core',
    'web.curator',
    'web.flags',
    'web.instances',
    'web.lists',
    'web.missions',
    'web.player_activities',
    'web.reports',
    'web.responses',
    'web.values',
    
    # Need this after web.admin because of test runner: 
    # it loads django admin tests by 'admin' app label first
    'django.contrib.admin',
    'django.contrib.admindocs',

    # 3rd party
    'django_mailer',
    'django_extensions',
    #'sentry',
    #'sentry.client',
    'gmapsfield',
    'gmapsfield.templatetags',
    'nani',
    #'dilla',
    'rosetta',
    'django_extensions',
    'south',
)

LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/'
MANAGERS = ADMINS
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
MEDIA_ROOT = os.path.join(DIRNAME, '../assets')
MEDIA_URL = '/assets/'

MIDDLEWARE_CLASSES = (
    'localeurl.middleware.LocaleURLMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
)

NOREPLY_EMAIL = 'noreply@communityplanit.org'
ROOT_URLCONF = 'web.urls'
SECRET_KEY = 'SET THIS IN settings.py'

SERIALIZATION_MODULES = {
    'yaml': "django.core.serializers.pyyaml"
} 

SERVER_EMAIL = 'noreply@communityplanit.org'
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SITE_ID = 1

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

TEMPLATE_DEBUG = True
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True

# Localization
LANGUAGE_CODE = 'en-us'
LOCALE_PATHS = (
        os.path.join(ROOTDIR, 'locale'),
)

ugettext = lambda s: s
LANGUAGES = (
  ('en-us', ugettext('English')),
  ('ht', ugettext(u'Haitian Creole')),
  ('es', ugettext(u'Spanish')),
)
#django-localeurl
LOCALE_INDEPENDENT_PATHS = (
    #re.compile('^/$'),
    re.compile('^/ajax/'),
    re.compile('^/comments/'),
    re.compile('^/__debug__/'),
    re.compile('^/assets/'),
    re.compile('^/static/'),
    re.compile('^/gr/'),
    re.compile('^/admin-media/'),
    re.compile('^/status/cache/'),
    re.compile('^/favicon.ico$'),
)
LOCALE_INDEPENDENT_MEDIA_URL = True
PREFIX_DEFAULT_LOCALE = True

#debug-toolbar
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS' : False,
}

#
# Community PlanIT settings
#

# Default points/coins
DEFAULT_POINTS = 10
DEFAULT_COINS = 0

#
# South settings
#
SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False

#
# Google Maps Field settings 
#
GMAP_DEFAULT = [42.355241376822725,-71.06010156250015] # Boston
GMAP_JQUERY = '/assets/3pty/js/jquery-1.4.4.min.js'

#Configure logging
LOGFILE = "cpi.log"
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=os.path.join(ROOTDIR, LOGFILE),
                    filemode='w')

logging.getLogger(__name__).setLevel(logging.INFO)
logging.info("cpi started")

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# settings can be overridden for testing; by default we use the in-memory
# sqlite database instead of PostgreSQL
if 'test' in sys.argv:
    try:
        from settings_test import *
    except ImportError:
        pass


