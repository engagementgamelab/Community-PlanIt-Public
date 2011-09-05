from os import path

PROJECT_ROOT = path.normpath(path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME' : path.join(PROJECT_ROOT, 'test.db'),
    }
}
