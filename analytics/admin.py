from django.contrib import admin

from analytics.models import TelegramUsers, Analytics


@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ('users_unique', 'number_of_clicks')

    def has_add_permission(self, request):
        return False


@admin.register(TelegramUsers)
class TelegramUsersAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
