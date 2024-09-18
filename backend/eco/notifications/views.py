"""Notifications views."""

import json

from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import PushSubscription


@csrf_exempt
def subscribe_info(request: HttpRequest) -> HttpResponse:
    """Subscribe info view.

    After subscribing to push notifications using the WebPush API, the frontend sends the subscription data to this view.
    """  # noqa: E501
    if request.method == "POST":
        subscription_data = json.loads(request.body)
        user = request.user if request.user.is_authenticated else None
        PushSubscription.objects.create(
            user=user,
            endpoint=subscription_data["endpoint"],
            p256dh=subscription_data["keys"]["p256dh"],
            auth=subscription_data["keys"]["auth"],
        )

        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)


def serviceworker(request: HttpRequest) -> HttpResponse:
    """Service worker view."""
    context = {
        "vapid_public_key": settings.VAPID_PUBLIC_KEY,
    }
    return render(
        request,
        "serviceworker.js",
        content_type="application/javascript",
        context=context,
    )
