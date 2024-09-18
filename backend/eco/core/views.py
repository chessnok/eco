from django.contrib.auth import login

from .models import Event
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserCreationForm, UserProfileForm
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
            return redirect('user_profile')  # Перенаправление после успешного сохранения
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'user_profile.html', {'form': form})
