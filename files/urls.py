from django.urls import path
from .views import file_load, file_write
from . import views

urlpatterns = [
    path('down/', file_write, name='file_write'),
    path('', file_load, name='file_load'),
]