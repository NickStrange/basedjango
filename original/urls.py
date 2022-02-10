from django.urls import path
from .views import home_original, upload_old_works, download_old_works
urlpatterns = [
    path('', home_original, name='home_original'),
    path('upload_old/', upload_old_works, name='upload_old_works'),
    path('download_old/', download_old_works, name='download_old_works'),
    ]
