from django.contrib import messages

from .models import Event, PromoCodeUsage
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserProfileForm, EventForm, PromoCodeActivationForm
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
    """
    Представление для отображения и редактирования профиля пользователя,
    а также отображения формы создания нового мероприятия и активации промокода.
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        promo_form = PromoCodeActivationForm(request.POST)

        if 'promo_code_submit' in request.POST:  # Если отправлена форма промокода
            if promo_form.is_valid():
                promo_code = promo_form.cleaned_data['code']
                try:
                    discount = promo_code.activate(request.user)
                    messages.success(request, f"Промокод активирован! Вы получили {discount} на баланс.")
                except ValueError as e:
                    messages.error(request, str(e))
            return redirect('user_profile')

        elif form.is_valid():  # Если отправлена форма профиля
            form.save()
            messages.success(request, "Профиль успешно обновлен!")
            return redirect('user_profile')

    else:
        form = UserProfileForm(instance=request.user)
        promo_form = PromoCodeActivationForm()

    event_form = EventForm(user=request.user)
    used_promocodes = PromoCodeUsage.objects.filter(user=request.user)

    return render(request, 'user_profile.html', {
        'user_form': form,
        'event_form': event_form,
        'promo_form': promo_form,
        'used_promocodes': used_promocodes,
        'balance': request.user.balance
    })


@login_required
def new_event(request):
    """
    Представление для создания нового мероприятия организатором.
    """
    if request.method == 'POST' and request.user.is_organizer and request.user.organizer.status == 'Confirmed':
        form = EventForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Мероприятие успешно создано!")
            return redirect('user_profile')
    else:
        form = EventForm(user=request.user)

    return render(request, 'user_profile.html', {
        'event_form': form,
        'user_form': UserProfileForm(instance=request.user),
        'promo_form': PromoCodeActivationForm(),
        'used_promocodes': PromoCodeUsage.objects.filter(user=request.user),
        'balance': request.user.balance
    })

def event(request, event_id):
    event = Event.objects.get(id=event_id)
    if not event or not event.is_published:
        return redirect('event_list')
    return render(request, 'event.html', {'event': event})
