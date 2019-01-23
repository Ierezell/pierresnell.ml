from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'blog'

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    # url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    path('post/<int:post_nb>/', views.post_detail, name='post_detail'),
    path('commenter/<int:post_nb>/', views.commenter, name='commenter'),
    path('new_post/', views.new_post, name='new_post'),
    path('edit_post/<int:post_nb>/', views.edit_post, name='edit_post')
]
