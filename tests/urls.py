from django.conf import settings as dj_settings
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(
        r'^admin/',
        admin.site.urls
    ),
    url(
        r'^for_test_app/',
        include(
            "vue_form_generator.tests.for_test.urls",
            namespace="for_test"
        )
    )
]


if dj_settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
