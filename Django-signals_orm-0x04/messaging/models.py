from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Messages(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recieved_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Notifications(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(
        Messages, on_delete=models.CASCADE, related_name='notifications')
    content = models.TextField()
