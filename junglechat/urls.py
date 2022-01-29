from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
urlpatterns = [
    path('', views.jungleland,name="jungleland"),
    url(r'^snips/', views.snippets.as_view()),
    path('quotes/', views.quotes.as_view()),
    path('quotes/<int:id>/<str:ip>/', views.quotes.as_view())
]
