from django.db import models
from django.contrib.auth.models import User

class UploadHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='history_uploads/')
    result = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']   # newest first

    def __str__(self):
        return f"{self.user.username} - {self.result} - {self.created_at:%Y-%m-%d %H:%M}"