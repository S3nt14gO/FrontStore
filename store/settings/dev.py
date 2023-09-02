from .common import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=t=-l=stt3du9(7qyi=8p^n9!1nkv%!bs%l#t-ce9&z%ia26k_'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'store',
        'USER': 'postgres',
        'PASSWORD': '0965211901',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}


