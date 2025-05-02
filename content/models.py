from django.db import models
from django.conf import settings

class Vlog(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    video = models.FileField(upload_to='vlogs/videos/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='vlogs/thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
