from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """Signal to create notification for a user when they have recieve a message"""
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_edit(sender, instance, **kwargs):
    """Signal to track message editing, log old message"""
    instance.edited = True
    MessageHistory.objects.create(
        message=instance, content=instance.content, edited_by=instance.user)
