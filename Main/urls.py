import re
from django.urls import path, re_path
from django.conf import settings

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.indexView, name='index'),
    path('upload', views.UploadView.as_view(), name='upload'),
    path('modifie', views.ModifieView.as_view(), name='modifie'),
    path('delete', views.deleteVideo, name='delete'),
    path('watch', views.watchView, name='watch'),
    path('playlist', views.PlaylistView.as_view(), name='playlist'),
    path('playlist/<str:id>/delete', views.deletePlaylistView, name='delete_playlist'),
    path('api/impression', views.submitImpressionView.as_view(), name='impressions'),
    path('api/playlists', views.ApiPlaylists.as_view(), name='playlists_api'),
    path('api/subscribe', views.SubscribeView.as_view(), name='subscribe'),
    path('api/submitview', views.submitViews, name='submit_view'),
    path('api/comment', views.ApiComments.as_view(), name='comments_api'),
]

if settings.DEBUG :
    urlpatterns += [
        re_path(r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')), views.staticView, name='media')
    ]