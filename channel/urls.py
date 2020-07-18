from django.urls import path

from . import views

app_name = 'channel'

urlpatterns = [
    path('<str:id>/', views.index, name='index'),
    path('<str:id>/modifie', views.ModifieChannel.as_view(), name='modifie'),
    path('<str:id>/videos', views.videosView, name='videos'),
    path('<str:id>/playlists', views.playlistsView, name='playlists'),
    path('<str:id>/about', views.aboutChannel, name='about'),
    path('<str:id>/subscriptions', views.subscriptionsChannel, name='subscriptions'),
]