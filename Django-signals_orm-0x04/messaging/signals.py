from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Messages, Notifications


@receiver(post_save, sender=Messages)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notifications.objects.create(
            user=instance.receiver, message=instance, content=f"New message from {instance.sender.username}")
