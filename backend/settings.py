from pathlib import Path
from datetime import timedelta
import os
import stripe

import environ
env = environ.Env()
environ.Env.read_env()


BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = os.getenv('SECRET_KEY')


DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
# CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:3000']


CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://dine-eazy.onrender.com',
]



INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    
    'rest_framework',
    'corsheaders',
    'user_api',
    'banner',
    
    'rest_framework_simplejwt.token_blacklist',
    'admin_api',
    'restaurant_api',
    'chat',
    'channels',
   
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'
ASGI_APPLICATION = "backend.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# # Database
# # https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# # DATABASES = {
# #     'default': {
# #         'ENGINE': 'django.db.backends.postgresql',
# #         'NAME': 'dbBooking',
# #         'USER': 'postgres',
# #         'PASSWORD': '12345',
# #         'HOST': 'localhost',
# #         'PORT': '5432',
# #     }
# # }

AUTH_USER_MODEL = 'user_api.AppUser'



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# # Internationalization
# # https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# # Static files (CSS, JavaScript, Images)
# # https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS=[os.path.join(BASE_DIR,'STATIC')]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'



# # Default primary key field type
# # https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # Add other authentication backends if needed
]

REST_FRAMEWORK = {
     'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ],
'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (      
        'rest_framework.permissions.AllowAny',
    ),
}
# STRIPE_SECRET_KEY='sk_test_tR3PYbcVNZZ796tH88S4VQ2u'
# STRIPE_SECRET_KEY='sk_test_51NSzh3SDJyz85wUkLBFeckRO9t412hqCmvq51zOy7KUCjqYGvXMjavOKDhAzF9DFZi7uyy4vwnkYqRNxp9XE5y2z00If07bIgQ'

STRIPE_SECRET_KEY='sk_test_51NXgQsSCyVsYvgIHxdAf6qcCP29fOQSC9SrVRlsrOO4dpnq9a0ShTuwkUS1m0nZVKA8P75CkkKkiQ03UHrdxURtE00AMr5YDX6'
STRIPE_PUBLISHABLE_KEY = 'pk_test_51NXgQsSCyVsYvgIHKQTU5wWDO1KjgOpAaUbnKv2nPcQnxecjXGsqMQY9hhWY0cphBjQVDOIip07tVpgQmRTpTkZL00zVXQjKp2'

STRIPE_WEBHOOK_SECRET='whsec_f2c01980ce49821659f913a878498b0ec28627129c54294beb3b0f2e9013a5e1'
 

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
}


# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#     'ROTATE_REFRESH_TOKENS': True,
#     'BLACKLIST_AFTER_ROTATION': True
# }

# TWILIO_ACCOUNT_SID = 'ACb890b2d828304ad1d52e615be9d000b7'
# TWILIO_AUTH_TOKEN = '88ec71f012ac26a558769555fcd164dd'
# TWILIO_PHONE_NUMBER = 'YOUR_TWILIO_PHONE_NUMBER'

# EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST='smtp.gmail.com'
# EMAIL_USE_TLS=True
# EMAIL_PORT=587
# EMAIL_HOST_USER='greatkart9@gmail.com'
# EMAIL_HOST_PASSWORD='rbgigvjvxnacblos'

EMAIL_BACKEND = env("EMAIL_BACKEND")
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', '').lower() == 'true'
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
