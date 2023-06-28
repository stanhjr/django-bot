from django.contrib import admin

from feedbacks.models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False
