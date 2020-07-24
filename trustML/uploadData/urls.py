from django.urls import path

from . import views

app_name = 'uploadData'
urlpatterns = [
    path('', views.index, name='index'),
]
