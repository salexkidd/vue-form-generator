import os

DEBUG = True

SECRET_KEY = "secret_key_for_testing"

ALLOWED_HOSTS = ["*"]

INTERNAL_IPS = "127.0.0.1"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'django_extensions',
    'webpack_loader',
    'rest_framework',
    'definable_serializer',
    'vue_form_generator.tests.for_test',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': './test.db',
    }
}

ROOT_URLCONF = 'tests.urls'

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'npm.finders.NpmFinder',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            "templates",
            os.path.join(BASE_DIR, "vue_form_generator", "templates"),
        ],
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

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (),
    'DEFAULT_AUTHENTICATION_CLASSES': (),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'vue_form_generator.renderers.VueFormGeneratorSchemaRenderer',
    ),
}

VUE_FORM_GENERATOR_SETTINGS = VUE_FORM_GENERATOR_SETTINGS = {
    "EXTERNAL_FIELD_AND_VUE_FORM_GENERATOR_MAP": {
        "definable_serializer.extra_fields.RadioField": {"type": "radios"},
        "definable_serializer.extra_fields.CheckRequiredField": {"type": "switch"},
        "definable_serializer.extra_fields.MultipleCheckboxField": {"type": "checklist"},
        "definable_serializer.extra_fields.ChoiceRequiredField": {
            "type": "vueMultiSelect",
            "selectOptions": {"key": "name", "label": "name",}
        },
        "definable_serializer.extra_fields.ChoiceWithBlankField": {
            "type": "vueMultiSelect",
            "selectOptions": {"key": "name", "label": "name",}
        }
    }
}
