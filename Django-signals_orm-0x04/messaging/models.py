from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Message(models.Model):
    parent_message = models.ForeignKey(Message,on_delete=models.CASCADE, related_name='reply')
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recieved_messages')
    content = models.TextField()
    edited = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, related_name='message_history')
    content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='edited_messages')
    
    class Meta:
        unique_together = (('message', 'timestamp'),)


class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='notifications')
