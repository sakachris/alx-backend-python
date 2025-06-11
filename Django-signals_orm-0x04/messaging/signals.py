# messaging/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        # New message, skip
        return

    try:
        original = Message.objects.get(pk=instance.pk)
        if original.content != instance.content:
            MessageHistory.objects.create(
                message=instance, old_content=original.content
            )
            instance.edited = True
    except Message.DoesNotExist:
        pass
