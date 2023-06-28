from django.urls import include, path
from rest_framework import routers
from shops.views import CityViewSet

router = routers.DefaultRouter()
router.register(r'shops', CityViewSet, basename='shops')

urlpatterns = [
    path('', include(router.urls)),
]
