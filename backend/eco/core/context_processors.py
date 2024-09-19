from core.models import Event


def global_context(request):
    return {
        'near_events': Event.objects.filter(is_published=True,)[:3],  # Example: Add user IP
    }
