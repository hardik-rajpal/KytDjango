from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views
urlpatterns = [
    path('', views.land,name="land"),
    path('submit', views.submit, name="submit")
]
