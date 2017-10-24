"""

#### THIS IS AN EXAMPLE FILE. CONFIG MUST BE PRESENT IN config.py FILE ####

This file stores all the things that are meant to be secret from the public
and settings that change from one computer to another. Configure the file
before running the Django application.
"""


SECRET_KEY = '1w(i86@y8@r$d%9_qyirf6d!*vo!49kx=1aok!br*((*@za!p('
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'crmdb',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '',
    }
}
