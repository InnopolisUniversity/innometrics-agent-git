from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
<<<<<<< HEAD

from activities import views

urlpatterns = [
=======
from activities import views

urlpatterns = [
    url(r'^$', views.ActivityList.as_view()),
>>>>>>> b08e6a3e8b2c2dd9bc6e05534b8e9593d0bb7dab
    url(r'^activities/$', views.ActivityList.as_view(), name='activities'),
    url(r'^activities/(?P<pk>[0-9]+)/$', views.ActivityDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
