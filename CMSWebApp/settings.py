"""
Django settings for CMSWebApp project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR/ ".env")

LOGIN_REDIRECT_URL = "profile"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
ADMINS = [("c2091021", "c2091021@hallam.shu")]
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = 'WEBSITE_HOSTNAME' not in os.environ
DEBUG= False

if DEBUG:
    ALLOWED_HOSTS = ["localhost","127.0.0.1","https://cmswepapp-c2091021.azurewebsites.net","cmswepapp-c2091021.azurewebsites.net"]
else:
    ALLOWED_HOSTS = ["https://cmswepapp-c2091021.azurewebsites.net","cmswepapp-c2091021.azurewebsites.net"]
    CSFR_TRUSTED_ORIGINS = ["https://cmswepapp-c2091021.azurewebsites.net"]


CRISPY_TEMPLATE_PACK = "bootstrap4"
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "WebApp.apps.WebappConfig",
    "users.apps.UsersConfig",
    "crispy_forms",
    "crispy_bootstrap4",
    "storages"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "CMSWebApp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "CMSWebApp.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {         
    "default": {             
        "ENGINE": "django.db.backends.mysql",            
        "NAME": os.environ.get("AZURE_DB_NAME"),          
        "HOST": os.environ.get("AZURE_DB_HOST"),             
        "PORT": os.environ.get("AZURE_DB_PORT"),             
        "USER": os.environ.get("AZURE_DB_USER"),             
        "PASSWORD": os.environ.get("AZURE_DB_PASSWORD"),  }  }




# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
if DEBUG:     
    STATIC_URL = "static/"     
    MEDIA_ROOT = BASE_DIR / "media"     
    MEDIA_URL = "/media/" 
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
else:     
    MEDIA_URL = f"https://{os.environ.get('AZURE_SA_NAME')}.blob.core.windows.net/media/"
    STATIC_URL = f"https://{os.environ.get('AZURE_SA_NAME')}.blob.core.windows.net/static/"
    DEFAULT_FILE_STORAGE = "CMSWebApp.storages.AzureMediaStorage"
    STATICFILES_STORAGE = "CMSWebApp.storages.AzureStaticStorage"
    AZURE_SA_NAME = os.environ.get("AZURE_SA_NAME")     
    AZURE_SA_KEY = os.environ.get("AZURE_SA_KEY")    
    STATIC_ROOT = BASE_DIR / "staticfiles"    
    MEDIA_ROOT = BASE_DIR / "mediafiles"



# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
