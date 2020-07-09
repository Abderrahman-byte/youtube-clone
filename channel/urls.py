from django.urls import path

from . import views

app_name = 'channel'

urlpatterns = [
    path('<str:id>/', views.index, name='index')
]