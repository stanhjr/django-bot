from rest_framework import serializers

from feedbacks.models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'text', 'is_read', 'created_at')
        read_only_fields = ('id', 'is_read', 'created_at')
