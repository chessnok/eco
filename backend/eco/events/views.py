from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.reverse import reverse

from notifications.actions import send_push_notification
from .models import UserModel
from .forms import OrganizerRegistrationForm


@login_required
def register_organizer(request):
    if request.method == 'POST':
        form = OrganizerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            organizer = form.save(commit=False)
            organizer.user = request.user
            organizer.status = 'WaitingForConfirmation'
            organizer.save()
            request.user.is_organizer = True
            request.user.save()
            admin_users = UserModel.objects.filter(is_staff=True,
                                                   user_permissions__codename="events.change_organizer")
            for admin in admin_users:
                send_push_notification(
                    user=admin,
                    message=f"Новая заявка на подтверждение организатора от {request.user.username}",
                    url=reverse('admin:events_organizer_change',
                                args=[organizer.pk]),
                )

            return redirect('user_profile')
    else:
        form = OrganizerRegistrationForm()

    return render(request, 'register_organizer.html', {'form': form})
