from pathlib import Path
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

try:
    from .local_settings import *
except ImportError:
    pass


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 追加Apps
    'rest_framework',
    'djoser',
    'api.apps.ApiConfig',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 追加Middleware
    'corsheaders.middleware.CorsMiddleware',
]

# Reactからのアクセス
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000'
]
ROOT_URLCONF = 'karaimonoyasan_api.urls'

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

WSGI_APPLICATION = 'karaimonoyasan_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'karaimonoyasan_api_db',
        'USER': 'root',
        'PASSWORD': '',
    }
}

# 閲覧権限の認証用
REST_FRAMEWORK = {
    # 特定ユーザーへの権限割当
    'DEFAULT_PERMISSION_CLASSES': [
        # ログイン時のみ閲覧可能な設定
        'rest_framework.permissions.IsAuthenticated',
    ],
    # 認証方法の指定
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # JWTでの認証
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# JWTの設定
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    # 認証有効時間の設定
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=3),
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
# MEDIAデータ格納パスの指定
MEDIA_ROOT = BASE_DIR.joinpath('media')
# ブラウザからのmediaリクエスト時のディレクトリ(パス)設定
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
