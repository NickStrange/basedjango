from django.urls import path
from .views import upload_old_works, view_old_works, download_old_works

urlpatterns = [
    path('', view_old_works, name='view_old_works'),
    path('upload/', upload_old_works, name='upload_old_works'),
    path('download/', download_old_works, name='download_old_works'),
]