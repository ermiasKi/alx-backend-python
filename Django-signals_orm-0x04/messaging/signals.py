from .models import Message, Notification, User
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, text=f"New message from {instance.sender.username}", message=instance)


@receiver(pre_save, sender=Message)
def MessageHistory(sender, instance, created, **kwargs):
    if created:
        before_edit = instance.content
        MessageHistory.objects.create(instance=instance, before_edit=before_edit)


@receiver(post_delete, sender=User)
def DeleteUser(sender, instance, **kwargs):
    message = Message.objects.filter(sender=instance) | Message.objects.filter(receiver=instance)
    message.delete()

    notification = Notification.objects.filter(user=instance)
    notification.delete()