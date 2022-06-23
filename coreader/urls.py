from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
urlpatterns = [
    path('login_user/', views.UserSet.as_view({'post':'loginUser'}),name='login'),
    path('books_by_user/',views.BookSet.as_view({'get':'fetchBookSummaryByUser'},name='books')),
    path('get_full_book/',views.BookSet.as_view({'get':'fetchFullBook'},name='full_book')),
    path('push_books/',views.BookSet.as_view({'post':'pushBooks'},name='push_books')),
    path('push_glossaries/',views.BookSet.as_view({'post':'pushGlossaries'},name='push_glossaries')),
    path('push_notes/',views.BookSet.as_view({'post':'pushNotes'},name='push_notes')),
    path('push_deletes/',views.BookSet.as_view({'post':'pushDeletes'},name='deletes')),
    path('get_user_details/',views.UserSet.as_view({'get':'getUserDetails'}),name='userdetails')
]
