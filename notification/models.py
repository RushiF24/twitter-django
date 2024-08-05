from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    source_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificationsUsers')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)