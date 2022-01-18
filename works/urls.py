from django.urls import path
from .views import upload_old_works, view_old_works, download_old_works, upload_works, download_works, view_works

urlpatterns = [
    path('old', view_old_works, name='view_old_works'),
    path('', view_works, name='view_works'),
    path('upload_old/', upload_old_works, name='upload_old_works'),
    path('download_old/', download_old_works, name='download_old_works'),
    path('upload/', upload_works, name='upload_works'),
    path('download/', download_works, name='download_works'),
]