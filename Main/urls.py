import re
from django.urls import path, re_path
from django.conf import settings

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.indexView, name='index'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('modifie/', views.ModifieViewView.as_view(), name='modifie')
]

if settings.DEBUG :
    urlpatterns += [
        re_path(r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')), views.staticView, name='media')
    ]