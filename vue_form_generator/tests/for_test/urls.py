from django.conf.urls import url, include
from . import views as for_test_views

app_name = "for_test"

# router = PickupSerializerRouter()
# router.register(r"answer", for_test_views.AnswerViewSet, "answer")

# urlpatterns = router.urls

urlpatterns = [
    url(
        r'^test-page/(?P<definition>.+)/$',
        for_test_views.TestForAllFieldView.as_view(),
        name='test-page'
    ),
    url(
        r'^test-api/(?P<definition>.+)/$',
        for_test_views.TestAPI.as_view(),
        name='test-api'
    ),

]
