from rest_framework import viewsets

from shops.models import City
from shops.serializers import CitySerializer


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.prefetch_related('addresses').all()
    serializer_class = CitySerializer
