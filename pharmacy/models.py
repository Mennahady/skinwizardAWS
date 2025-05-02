
from django.db import models

# Create your models here.

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    manufacturer = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='medicine_images/', blank=True, null=True)  # ← Added
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name