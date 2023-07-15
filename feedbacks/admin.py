from django.contrib import admin

from feedbacks.models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'is_read', 'message_created')

    def has_add_permission(self, request):
        return False

    def message_created(self, instance: Feedback) -> str:
        if not instance.created_at:
            return ''
        return instance.created_at.strftime('%Y-%m-%d %H:%M:%S')

