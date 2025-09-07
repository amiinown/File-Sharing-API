from django.db import models
from folder.models import Folder
from group.models import Group
from django.conf import settings
from common.utils.file_path_in_bucket import create_file_path

class File(models.Model):
    title = models.CharField(max_length=255)
    original_name = models.CharField(max_length=255, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='files')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, blank=True, null=True, related_name='files')
    version = models.PositiveSmallIntegerField(default=1, editable=False)
    uploaded_file = models.FileField(upload_to=create_file_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args,**kwargs):
        if not self.pk:
            self.original_name = self.uploaded_file.name

            same_files_at_path = File.objects.filter(
                original_name=self.original_name,
                owner=self.owner,
                folder=self.folder,
                group=self.group,
                )
            if same_files_at_path.exists():
                max_version = same_files_at_path.aggregate(models.Max('version'))['version__max']
                self.version = max_version + 1 if max_version is not None else 1

        super().save(*args, **kwargs)