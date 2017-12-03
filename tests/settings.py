INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'rest_framework',
    'definable_serializer',
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
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}


SECRET_KEY = "secret_key_for_testing"
ROOT_URLCONF = 'tests.urls'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'libs.vue_form_generator.renderers.VueFormGeneratorSchemaRenderer',
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
