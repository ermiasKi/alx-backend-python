from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

# Create your models here.


class user(models.Model):
    ROLES = [
        ('guest', 'guest'),
        ('admin', 'admin'),
        ('host', 'host'),
    ]

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLES, default='guest')
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)

    class Meta:
        db_table = 'user'
        indexes = [
            models.Index(fields=['email']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email'),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"



class conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    participants_id = models.ForeignKey(user, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"conversation {self.conversation_id}"
    



class message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    sender_id = models.ForeignKey(user, on_delete=models.CASCADE)
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.email} at {self.sent_at}"