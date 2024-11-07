from .base import *


DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'istombroker',
        'USER': 'itom',
        "PASSWORD": "1",
        "HOST": "localhost",
        "PORT": 5432,
    }
}