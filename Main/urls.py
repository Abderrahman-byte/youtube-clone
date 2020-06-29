from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.indexView, name='index'),
    path('upload', views.UploadView.as_view(), name='upload')
]