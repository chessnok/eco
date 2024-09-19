from .models import Event
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserProfileForm, EventForm
from rest_framework import generics
from .serializers import EventSerializer


@login_required
def event_list(request):
    user_location = request.GET.get('location', None)  # Локация пользователя
    if user_location:
        events = Event.objects.filter(
            location__icontains=user_location)  # Фильтрация по локации
    else:
        events = Event.objects.all()  # Если локация не указана, выводим все

    context = {
        'events': events,
    }
    return render(request, 'event_list.html', context)


class EventListAPIView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(
                'user_profile')  # Перенаправление после успешного сохранения
    else:
        form = UserProfileForm(instance=request.user)
    event_form = EventForm(user=request.user)
    return render(request, 'user_profile.html', {
        'user_form': form,
        'event_form': event_form,
    })


@login_required
def new_event(request):
    if request.method == 'POST' and request.user.is_organizer and request.user.organizer.status == 'Confirmed':
        form = EventForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = EventForm(user=request.user)

    return render(request, 'user_profile.html', {
        'event_form': form,
        'user_form': UserProfileForm(instance=request.user),
    })


def event(request, event_id):
    event = Event.objects.get(id=event_id)
    if not event or not event.is_published:
        return redirect('event_list')
    return render(request, 'event.html', {'event': event})
