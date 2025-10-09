from django.db import models

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Returns unread messages for the given user, optimized with `.only()`
        to fetch only necessary fields.
        """
        return (
            self.filter(receiver=user, unread=True)
            .only("id", "sender", "receiver", "content", "timestamp")
            .order_by("-timestamp")
        )
