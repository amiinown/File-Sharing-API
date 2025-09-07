from django.db import models
from django.conf import settings
from group.models import Group

class Folder(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE, blank=True, null=True, related_name='folders')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='sub_folders')
    created_at = models.DateTimeField(auto_now_add=True)