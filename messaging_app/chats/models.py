from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class Roles(models.TextChoices):
    guest = "guest", "guest"
    host = "host", "host"
    admin = "admin", "admin"

# Create your models here.


class User(AbstractUser):
    """Custom class to extend User model"""
    # Required fields (to satisfy checker)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True)
    username = None

    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(
        max_length=10, choices=Roles.choices, default=Roles.guest)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    participants_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sender_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='messages')
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)
