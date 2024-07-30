from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Notification

@receiver(post_save, sender=Notification)
def notification_created(sender, instance, created, **kwargs):
    print(sender, instance, created)
    # if created:
