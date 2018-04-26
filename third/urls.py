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
    url(r'^tool/(?P<tool_name>\w+)/$', views.toolname, name='toolname'),
    ##博客详情链接
    url(r'^post/(?P<post_id>\d+)/$', views.detail, name='detail'),
    ##文章归档链接
    url(r'^post/archives/(?P<year>\d+)/(?P<month>\d+)/$', views.archives, name='archives'),
    ##文章分类链接
    url(r'^post/category/(?P<category_id>\d+)/$', views.category, name='category'),
    ##文章评论
    url(r'^post/comment/(?P<post_id>\d+)/$', views.post_comment, name='post_comment'),
    ##文章标签链接
    url(r'^post/tag/(?P<tag_id>\d+)/$', views.tag, name='tag'),
    url(r'^search/$', views.search, name='search'),

]