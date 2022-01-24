from django.urls import path
from .views import upload_old_works, view_old_works, download_old_works, upload_works, download_works, \
    view_work, work_home, clear_work, create_work, work_edit, work_delete

urlpatterns = [
    path('old', view_old_works, name='view_old_works'),
    path('', work_home, name='works_home'),
    path('work/<int:id>', view_work, name='view_work'),
    path('upload_old/', upload_old_works, name='upload_old_works'),
    path('download_old/', download_old_works, name='download_old_works'),
    path('upload/', upload_works, name='upload_works'),
    path('download/', download_works, name='download_works'),
    path('clear-work/',clear_work, name='clear-work'),
    path('create-work', create_work, name='create-work'),

    path('edit-work/<id>', work_edit, name='edit-work'),
    path('delete-work/<id>', work_delete, name='delete-work'),
]