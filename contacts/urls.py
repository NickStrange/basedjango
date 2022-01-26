from django.contrib import admin
from django.urls import path
from .views import home_contacts, contact_edit, create_contact, \
    contact_delete, sort_contact, reverse_sort_contact, load_contacts, clear_contact

urlpatterns = [
    path('', home_contacts, name='home_contacts'),
    path('edit_contact/<id>',contact_edit, name='edit_contact'),
    path('create_contact',create_contact, name='create_contact'),
    path('delete_contact/<id>',contact_delete, name='delete_contact'),
    path('sort_contact/<str:column>',sort_contact, name='sort_contact'),
    path('reverse_sort_contact/<str:column>',reverse_sort_contact, name='reverse_sort_contact'),
    path('load_contact/',load_contacts, name='load_contacts'),
    path('clear_contact/',clear_contact, name='clear_contact'),

]