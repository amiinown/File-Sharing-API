from django.db import models
from folder.models import Folder
from group.models import Group
from django.conf import settings
from utils import create_file_path

class File(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='files')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, blank=True, null=True, related_name='files')
    created_at = models.DateTimeField(auto_now_add=True)

class FileVersion(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='versions')
    version = models.CharField(max_length=20)
    uploaded_file = models.FileField(upload_to=create_file_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
