from django.contrib import admin
from django.urls import path
from .views import home_chooser
urlpatterns = [
    path('', home_chooser, name='home_chooser')
    ]
