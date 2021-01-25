"""
Django settings for noteplus project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '39x5e944lq!gux!7o*l8y^sc)=+t21$$cv@lm&2oog=(it0y55'

# SECURITY WARNING: don't run with debug turned on in production!
# 要想显示404页面，必须关闭debug
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	# #     自定义的应用  需要手动加入(如果该应用中有model表的定义的话，如果没有，可以不加入 )
	'common.apps.CommonConfig',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	# 开发调试过程中，先不用csrf校验
	# 'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'noteplus.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		# 模板的位置
		'DIRS': [BASE_DIR / 'templates']
		,
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

WSGI_APPLICATION = 'noteplus.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
		'NAME': 'noteplus',  # 数据库名，先前创建的
		'USER': 'root',  # 用户名，可以自己创建用户
		'PASSWORD': 'lishuai4899',  # 密码
		'HOST': '209.141.62.113',  # mysql服务所在的主机ip   这里改为远程主机
		'PORT': '3306',  # mysql服务端口
	}

	# 'default': {
	# 	'ENGINE': 'django.db.backends.sqlite3',
	# 	'NAME': BASE_DIR / 'db.sqlite3',
	# }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Shanghai'
# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

# USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/source/'
STATICFILES_DIRS =(os.path.join(os.path.dirname(__file__),'../source/').replace('\\','/'),)
# 设置js
import mimetypes

mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')


