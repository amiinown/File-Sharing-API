from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.core.validators import MinValueValidator, MaxValueValidator
import random
from django.utils import timezone
from datetime import timedelta


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = UserManager()

    def __ser__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
            return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff
    
class Otp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(9999)],
        editable=False,
        unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        expired_minutes_time = 1
        return self.created_at + timedelta(minutes=expired_minutes_time) < timezone.now()

    def save(self, **kwargs):
        if not self.pk:
            for _ in range(10):
                otp_code = random.randint(1000, 9999)
                same_otp_code = Otp.objects.filter(otp_code=otp_code)
                if not same_otp_code.exists():
                    self.otp_code = otp_code
                    break
            else:
                raise ValueError("Can't make an otp code.")
        super().save(**kwargs)