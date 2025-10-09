import uuid
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(max_length=20)

    password_hash = models.CharField(max_length=50)

    ROLES = [
        ('guest', 'guest'),
        ('admin', 'admin'),
        ('host', 'host'),
    ]

    role = models.CharField(max_length=20, choices=ROLES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name

class Conversation(models.Model):
    Conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    participants = models.ManyToManyField(User, related_name='conversation_participant')
    created_at = models.DateTimeField(auto_now_add=True)
    


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='edited_messages')
    edited = models.BooleanField(default=False)

    pre_save.connect(lambda sender, instance, **kwargs: setattr(instance, 'edited', True) if instance.pk else None)
    post_save.connect(lambda sender, instance, created, **kwargs: print(f"Message sent from {instance.sender} to {instance.receiver} at {instance.timestamp}"))

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    text = models.CharField(max_length=255)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    post_save.connect(lambda sender, instance, created, **kwargs: print(f"Notification for {instance.user}: {instance.message}"))