from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path
from server import views


urlpatterns = [
    url(r'^$', view=views.callback, name='callback'),
    url(r'^user$', view=views.userCallback, name='userCallback'),
]
