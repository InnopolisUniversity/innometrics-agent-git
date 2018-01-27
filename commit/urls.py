
from django.conf.urls import url
from commit import views

urlpatterns = [
    url(r'^githubuser/$', views.user_form),
    url(r'^search/$', views.search),
    url(r'^chart/$', views.chart),
    url(r'^graph/$', views.get_image)
]