from django.contrib import admin
from django.urls import path
from .views import home_chooser
urlpatterns = [
    path('/<str:home_type>', home_chooser, name='home_chooser')
    ]
