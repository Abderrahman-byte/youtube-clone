from django.urls import path

from . import views

app_name = 'channel'

urlpatterns = [
    path('<str:id>/', views.index, name='index'),
    path('<str:id>/modifie', views.ModifieChannel.as_view(), name='modifie'),
]