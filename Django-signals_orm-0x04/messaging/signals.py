from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification, User


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


@receiver(post_delete, sender=User)
def delete_related(sender, instance, **kwargs):

    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()
    Notification.objects.filter(user=instance).delete()
