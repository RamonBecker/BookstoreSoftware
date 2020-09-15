from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views


urlpatterns = [
    path('', include('blog.urlsView')),
]

