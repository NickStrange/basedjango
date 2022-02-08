from django.urls import path
from .views import download_works, \
    view_work, home_works, clear_work, create_work, edit_work, delete_work, work_sort, \
    work_reverse_sort, upload_works, work_test


urlpatterns = [
    path('', home_works, name='home_works'),
    path('test', work_test, name='test_work'),
    path('work/<int:id>', view_work, name='view_work'),
    path('upload/', upload_works, name='upload_works'),
    path('download/', download_works, name='download_works'),
    path('clear-work/', clear_work, name='clear_work'),
    path('create-work', create_work, name='create_work'),
    path('edit-work/<id>', edit_work, name='edit_work'),
    path('delete-work/<id>', delete_work, name='delete_work'),
    path('sort-work/<str:column>', work_sort, name='sort_work'),
    path('reverse-sort-work/<str:column>', work_reverse_sort, name='reverse_sort_work'),
]
