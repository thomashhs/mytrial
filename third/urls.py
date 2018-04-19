from django.conf.urls import url

from . import views

app_name='third'
urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^about/$', views.about, name='about'),
    url(r'^tool/$', views.tool, name='tool'),
    url(r'^tool/(?P<tool_name>\w+)/$', views.test, name='test'),
]