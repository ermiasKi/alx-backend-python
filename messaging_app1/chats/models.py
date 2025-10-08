import uuid
from django.db import models
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
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_message')
    Conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='conersation_group')

    message_body = models.TextField(null=False, blank=False)
    sent_at =  models.DateTimeField(auto_now_add=True)
    