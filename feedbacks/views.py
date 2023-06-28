from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from feedbacks.models import Feedback
from feedbacks.serializers import FeedbackSerializer


class FeedbackViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        if not request.META.get('HTTP_TELEGRAM_ID'):
            raise ValidationError("token header is missing.")
        return super().create(request, *args, **kwargs)

