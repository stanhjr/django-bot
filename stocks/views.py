from rest_framework import viewsets

from stocks.models import Stock
from stocks.serializers import StockSerializer


class StockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def get_queryset(self):
        return self.queryset.filter(is_active=True)

