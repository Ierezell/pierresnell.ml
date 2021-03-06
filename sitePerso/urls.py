from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'sitePerso'

urlpatterns = [

    path('post_list', views.post_list, name='post_list'),
    path('last_posts', views.last_posts, name='last_posts'),
    # url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    path('', views.acceuil, name='acceuil'),
    path('post/<int:post_nb>/', views.post_detail, name='post_detail'),
    path('commenter/<int:post_nb>/', views.commenter, name='commenter'),
    path('new_post/', views.new_post, name='new_post'),
    path('edit_post/<int:post_nb>/', views.edit_post, name='edit_post'),
    path('professional', views.professional, name='professional'),
    path('things', views.things, name='things'),
    path('projets', views.projets, name='projets'),
    path('contact', views.contact, name='contact'),
    path('files/<str:path>', views.view_files, name='files'),
    path('files/', views.view_files, name='files'),
    path('download/<str:path>', views.download, name='download'),
]
