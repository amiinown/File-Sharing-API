from django.db.models.signals import pre_save
from django.dispatch import receiver
from accounts.models import Otp

@receiver(pre_save, sender=Otp)
def delete_pre_otp_row(sender, instance, **kwargs):
    otp_exists = Otp.objects.filter(user=instance.user).exclude(pk=instance.pk).first()
    if otp_exists:
        otp_exists.delete()