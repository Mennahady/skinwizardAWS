from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'DOCTOR')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
    )
    
    username = None  # Remove username field
    email = models.EmailField(_('email address'), unique=True)  # Make email the USERNAME_FIELD
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='PATIENT')
    
    # Doctor specific fields
    id_number = models.CharField(max_length=50, blank=True, null=True, help_text='National ID or License number')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default
    
    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.email} ({self.user_type})"

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'accounts_customuser'  # Explicitly set the table name
        swappable = 'AUTH_USER_MODEL'

# --------------------
# Pharmacy Profile
# --------------------
class PharmacyProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='pharmacy_profile')
    pharmacy_name = models.CharField(max_length=255)
    address = models.TextField()
    license = models.ImageField(upload_to='licenses/')

    def __str__(self):
        return f"Pharmacy: {self.pharmacy_name}"
