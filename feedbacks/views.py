from rest_framework import  mixins
from rest_framework.viewsets import GenericViewSet

from feedbacks.models import Feedback
from feedbacks.serializers import FeedbackSerializer


class FeedbackViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

