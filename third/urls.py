from django.conf.urls import url

from . import views

app_name='third'
urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^test/$', views.test, name='test'),
]