from django.contrib import admin

from .models import Organizer


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization_name', 'user', 'status']
    list_filter = ['status']
    search_fields = ['organization_name', 'user__email']
    readonly_fields = ['id', 'created_at', 'organization_name',
                       'registration_date', 'org_type',
                       'address', 'data_fetched_at']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields += ['ogrn', 'documents', 'user']
        return self.readonly_fields

    fieldsets = (
        ("Системная информация", {
            "fields": (
                'id', 'created_at', 'status', 'data_fetched_at',
            )
        },),
        ("Организатор", {
            "fields": (
                'organization_name', 'ogrn', 'registration_date', 'org_type',
                'address',
            )
        },),
        ("Документы для проверки", {
            "fields": (
                'documents',
            )
        },),
        ("Пользователь", {
            "fields": (
                'user',
            )
        },),
    )
