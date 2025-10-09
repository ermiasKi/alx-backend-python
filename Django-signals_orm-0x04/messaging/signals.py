from .models import Message, Notification, User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, text=f"New message from {instance.sender.username}", message=instance)