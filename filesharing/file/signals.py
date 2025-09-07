from .models import File
from django.db.models.signals import post_delete
from django.dispatch import receiver

@receiver(signal=post_delete, sender=File)
def delete_file_from_s3(sender, instance, **kwargs):
    if instance.uploaded_file:
        instance.uploaded_file.delete(save=False)