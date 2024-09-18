"""Actions for sending push notifications."""

import json

from django.contrib.auth.models import User

from notifications.models import PushSubscription

from pywebpush import WebPushException, webpush

from symptomato import settings


def send_push_notification(user: User, message: str, url: str = None) -> None:
    """Send push notification to user."""
    subscriptions = PushSubscription.objects.filter(user=user)

    for subscription in subscriptions:
        subscription_info = {
            "endpoint": subscription.endpoint,
            "keys": {"p256dh": subscription.p256dh, "auth": subscription.auth},
        }
        try:
            webpush(
                subscription_info=subscription_info,
                data=json.dumps({"message": message, "url": url or ""}),
                vapid_private_key=settings.VAPID_PRIVATE_KEY,
                vapid_claims={"sub": f"mailto:{settings.VAPID_ADMIN_EMAIL}"},
            )
        except WebPushException as ex:
            print(f"Ошибка отправки уведомления: {ex}")
