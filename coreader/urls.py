from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
urlpatterns = [
    path('login/', views.UserAuth.as_view({'post':'login'}),name='login'),
    path('books_by_user/',views.BookSet.as_view({'get':'fetchBookSummaryByUser'},name='books'))
]
