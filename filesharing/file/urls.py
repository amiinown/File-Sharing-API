from django.urls import path
from .views import AddFileView, DeleteFileView, DownloadFileView, ListFileView

app_name = 'files'
urlpatterns = [
    path('list/', ListFileView.as_view(), name='list_files'),
    path('add/', AddFileView.as_view(), name='add-file'),
    path('download/<int:file_id>/', DownloadFileView.as_view(), name='download-file'),
    path('remove/<int:file_id>/', DeleteFileView.as_view(), name='remove-file'),
]