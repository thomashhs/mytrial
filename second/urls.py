from django.conf.urls import url

from . import views

app_name='second'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<title_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<title_id>[0-9]+)/results/$', views.result, name='result'),
    url(r'^(?P<title_id>[0-9]+)/(?P<meeting_id>[0-9]+)/delete/$', views.delete, name='delete'),
]