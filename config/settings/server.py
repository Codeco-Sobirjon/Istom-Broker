from .base import *


DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'istombroker',
        'USER': 'postgres',
        "PASSWORD": "0576",
        "HOST": "localhost",
        "PORT": 5432,
    }
}