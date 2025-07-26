from django.db import models
from django.contrib.auth.models import AbstractUser


class Roles(models.TextChoices):
    guest = "guest", "guest"
    host = "host", "host"
    admin = "admin", "admin"

# Create your models here.


class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True)
    email = models.EmailField(unique=True)
    username = None
    
    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(
        max_length=10, choices=Roles.choices, default=Roles.guest)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True)
    sender_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True)
    participants_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
