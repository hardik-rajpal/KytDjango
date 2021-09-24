from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views
urlpatterns = [
    path('', views.land,name="land"),
    path('submit', views.submit, name="submit"),
    path('checkstatus/', views.check_status, name="check_status"),
    path('resang', views.results, name='resang'),
    path('data/', views.dataHandler.as_view(), name="data")
]
