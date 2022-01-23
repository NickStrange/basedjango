from django.contrib import admin
from django.urls import path
from .views import home, contact_edit, create_contact, contact_delete, contact_sort, contact_reverse_sort, load_contacts, clear_contact

urlpatterns = [
    path('home/', home, name='contacts-home'),
    path('edit-contact/<id>',contact_edit, name='edit-contact'),
    path('create-contact',create_contact, name='create-contact'),
    path('delete-contact/<id>',contact_delete, name='delete-contact'),
    path('sort-contact/<str:column>',contact_sort, name='sort-contact'),
    path('reverse-sort-contact/<str:column>',contact_reverse_sort, name='reverse-sort-contact'),
    path('load-contact/',load_contacts, name='load-contact'),
    # path('search-contact',search_contact, name='search-contact'),
    path('clear-contact/',clear_contact, name='clear-contact'),

    path('', home, name='post-create'),
    path('', home, name='contacts-about'),
    path('', home),
    path('', home, name='login'),
    path('', home, name='register'),
    path('', home, name='profile'),
    path('', home, name='logout'),
]