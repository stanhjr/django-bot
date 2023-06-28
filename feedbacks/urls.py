from django.urls import include, path
from rest_framework import routers
from feedbacks.views import FeedbackViewSet

router = routers.DefaultRouter()
router.register(r'feedback', FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('', include(router.urls)),
]
