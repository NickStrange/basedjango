from django.contrib import admin
from django.urls import path
from .views import home_contacts, contact_edit, create_contact, \
    contact_delete, sort_contact, reverse_sort_contact, load_contacts, clear_contact, download_contacts, contact_view

urlpatterns = [
    path('', home_contacts, name='home_contacts'),
    path('view_contact/<int:id>/<ids>', contact_view, name='contact_view'),
    path('edit_contact/<id>', contact_edit, name='contact_edit'),
    path('create_contact', create_contact, name='create_contact'),
    path('delete_contact/<id>', contact_delete, name='contact_delete'),
    path('sort_contact/<str:column>', sort_contact, name='sort_contact'),
    path('reverse_sort_contact/<str:column>', reverse_sort_contact, name='reverse_sort_contact'),
    path('load_contact/', load_contacts, name='load_contacts'),
    path('download_contacts/', download_contacts, name='download_contacts'),
    path('clear_contact/', clear_contact, name='clear_contact'),
]
