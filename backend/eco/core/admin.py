from django.contrib import admin

from .models import Event, UserModel, BotTicket, BotUser


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'status', 'is_published')
    list_filter = ('status', 'is_published', 'date')
    search_fields = ('name', 'description')
    date_hierarchy = 'date'
    ordering = ('-date',)

    fieldsets = (
        (None, {'fields': (
            'name', 'date', 'description', 'status',
            'is_published',
            'latitude', 'longitude')}),
    )


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'age', 'home_address', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'home_address')
    list_filter = ('is_active', 'is_staff')
    ordering = ('username',)
    readonly_fields = ('last_login',)

    fieldsets = (
        (None, {'fields': (
            'username', 'password', 'email', 'first_name', 'last_name')}),
        ('Personal Info', {'fields': ('age', 'home_address')}),
        ('Permissions', {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'user_permissions',
            'groups')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )


# Регистрация модели BotUser
@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    # Отображаемые поля на странице списка пользователей бота
    list_display = ('id', 'tg_id', 'longitude', 'latitude', 'has_location')

    # Фильтры для панели администратора
    list_filter = ('has_location',)

    # Поля для редактирования на странице пользователя бота
    fields = ('tg_id', 'longitude', 'latitude', 'has_location')

    search_fields = ('tg_id',)
    ordering = ('tg_id',)


# Регистрация модели BotTicket
@admin.register(BotTicket)
class BotTicketAdmin(admin.ModelAdmin):
    # Отображаемые поля на странице списка тикетов
    list_display = ('id', 'bot_user', 'mark')

    # Фильтры для панели администратора
    list_filter = ('mark',)

    # Поля для редактирования на странице тикета
    fields = ('bot_user', 'mark')

    search_fields = ('bot_user__tg_id',)
    ordering = ('bot_user',)
