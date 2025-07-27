from django.db import models
from django.conf import settings


class Group(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='groups', through='UserGroupPermission')
    created_at = models.DateTimeField(auto_now_add=True)


class UserGroupPermission(models.Model):

    class Role(models.TextChoices):
        READ = 'READ', 'Read'
        READ_WRITE = 'READ_WRITE', 'Read & Write'

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    permission = models.CharField(max_length=20, choices=Role.choices, default=Role.READ)

    class Meta:
        unique_together = ('user', 'group')