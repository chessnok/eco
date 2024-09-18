from django.urls import path
from django.views.generic import TemplateView

from .views import event_list, user_profile, new_event

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),

    # Страница списка мероприятий
    path('events/', event_list, name='event_list'),
    path('profile/', user_profile, name='user_profile'),
    path('new_event/', new_event, name='new_event'),

]
