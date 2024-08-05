# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from .models import Notification
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
from .serializers import NotificationListSerializer

@receiver(post_save, sender=Notification)
def notification_created(sender, instance, created, **kwargs):
    print("here from signals ",sender, instance.source_user_id, created)
    if created:
        channel_layer = get_channel_layer()

        serializer = NotificationListSerializer(instance)
        async_to_sync(channel_layer.group_send)(
            # 'notification_to_user',
            f'notification_from_{instance.user_id}_to_user',
                {
                    "type": "send_notification",
                    "notification": serializer.data
                }
        )
