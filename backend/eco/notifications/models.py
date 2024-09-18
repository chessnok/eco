"""Notifications models."""

from django.conf import settings
from django.db import models


class PushSubscription(models.Model):
    """Push subscription model."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    endpoint = models.TextField()
    p256dh = models.CharField(max_length=255)
    auth = models.CharField(max_length=255)

    def __str__(self):
        """Return string representation."""
        return f"PushSubscription for {self.user}"
