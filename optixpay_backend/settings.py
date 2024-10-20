from pathlib import Path
import os
from decouple import config
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', 'yd2f8slb8^+vrm3rb%9&!q=-$z1x5cq80ulqyb1_c3$yxl@=2b')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS = []

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')

# if 'CODESPACE_NAME' in os.environ:
#     codespace_name = config("CODESPACE_NAME")
#     codespace_domain = config("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN")
#     CSRF_TRUSTED_ORIGINS = [f'https://{codespace_name}-8000.{codespace_domain}']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # App
    'app_auth',
    'core',
    'app_transaction',
    'app_merchant',
    'app_payment',
    'app_agent',

    # Additional Libraries
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'corsheaders',
    'simple_history'
]

X_FRAME_OPTIONS = "ALLOW-FROM preview.app.github.dev"

AUTH_USER_MODEL = 'app_auth.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'simple_history.middleware.HistoryRequestMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'optixpay_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'optixpay_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if not DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
            'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

# Bkash Credential
BKASH_APP_KEY = 'E8QGBD19aGNfjYVmKgqfo9f1tc'
BKASH_APP_SECRET = 'tXTvohbA80UW0qtQazY2xGrEMuxW9uBto7oiwpJQWptFGXOR4gyZ'
BKASH_USERNAME = '01945503874'
BKASH_PASSWORD = '4CSX@Wr[I7B'
BKASH_BASE_URL = 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/'

# Path to the root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define the paths to your key files
NAGAD_MERCHANT_PUBLIC_KEY_PATH = os.path.join(BASE_DIR, 'keys', 'Merchant_MC00VHB20088378_1729337532364_pub.pem')
NAGAD_GATEWAY_PUBLIC_KEY_PATH = os.path.join(BASE_DIR, 'keys', 'Payment_Gateway_PublicKey.pem')
NAGAD_MERCHANT_PRIVATE_KEY_PATH = os.path.join(BASE_DIR, 'keys', 'Merchant_MC00VHB20088378_1729337532364_pri.pem')

# settings.py
NAGAD_CALLBACK_URL = "https://dnacell.shop/nagad-pay/payment/confirmation/"
# NAGAD_MERCHANT_PUBLIC_KEY_PATH = "/static/Merchant_MC00VHB20088378_1729337532364_pub.pem"
# NAGAD_GATEWAY_PUBLIC_KEY_PATH = "/static/Payment_Gateway_PublicKey.pem"
NAGAD_MERCHANT_ID = "68936101055331"
# NAGAD_MERCHANT_PRIVATE_KEY_PATH = "/static/Merchant_MC00VHB20088378_1729337532364_pri.pem"
NAGAD_BASE_URL = "https://api.nagad.com.bd"



# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#     BASE_DIR / "static",  # If you have custom static files
# ]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # This is the directory where collected static files will be stored


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOWED_ORIGINS = [
#     "https://example.com",
#     "https://sub.example.com",
#     "http://localhost:8080",
#     "http://127.0.0.1:9000",
# ]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=180),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

EMAIL_HOST = 'smtp.hostinger.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'no-reply@optixpay.com'
EMAIL_HOST_PASSWORD = 'u3P#xEfPD!8PPLX'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'no-reply@optixpay.com'

# MinIO server connection details
MINIO_STORAGE_ENDPOINT = '147.79.66.187:9000'  # IP address and port of the MinIO server
MINIO_STORAGE_ACCESS_KEY = "DlDYlIh7zzodF08GfMj4"
MINIO_STORAGE_SECRET_KEY = "rZ8kB1B010XJYtF5eTkgTp1Dplncw5tC0eBonQjP"
MINIO_STORAGE_BUCKET_NAME = 'optixpaybucket'  # The bucket name in MinIO

