from django.urls import path
from .views import AddFolderView, DeleteFolderView


app_name = 'folders'
urlpatterns = [
    path('add/', AddFolderView.as_view(), name='add-folder'),
    path('remove/<int:folder_id>/', DeleteFolderView.as_view(), name='remove-folder'),
]