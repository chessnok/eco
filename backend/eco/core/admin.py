from django.contrib import admin
from .models import Event, UserModel

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'status', 'is_published')
    list_filter = ('status', 'is_published', 'date')
    search_fields = ('name', 'description', 'location')
    date_hierarchy = 'date'
    ordering = ('-date',)

    fieldsets = (
        (None, {'fields': ('name', 'date', 'description', 'location', 'status', 'is_published', 'latitude', 'longitude')}),
    )

@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'age', 'home_address', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'home_address')
    list_filter = ('is_active', 'is_staff')
    ordering = ('username',)
    readonly_fields = ('last_login',)

    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'first_name', 'last_name')}),
        ('Personal Info', {'fields': ('age', 'home_address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
