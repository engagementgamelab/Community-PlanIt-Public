#!/usr/bin/env python

from random import choice
import sys

TEMPLATE = """
from settings_base import *

ADMINS = (
    ('%(admin_name)s', '%(admin_email)s'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cpi',
        'USER': 'cpi',
        'PASSWORD': '%(database_password)s'
    }
}

MANAGERS = ADMINS

SECRET_KEY = '%(secret_key)s'

if 'test' in sys.argv:    
    try:
	from settings_test import *        
    except ImportError:        
	pass
"""

if len(sys.argv) != 2:
    print "Usage: python make_settings.py <settings_filename.py>"
    sys.exit(1)

print sys.argv[1]

admin_name = raw_input("Your name: ")
admin_email = raw_input("Your email address: ")
database_password = raw_input("The database password: ")

settings = TEMPLATE % {
    'secret_key': ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)]),
    'admin_name': admin_name,
    'admin_email': admin_email,
    'database_password': database_password
}


f = open(sys.argv[1], 'w')
f.write(settings)
f.close()
