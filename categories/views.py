from rest_framework import viewsets
from rest_framework.response import Response

from categories.models import Category
from categories.serializers import CategorySerializer, CategoryNameSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryNameSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Category.objects.filter(parent__isnull=True).all()

        return Category.objects.all()

    def retrieve(self, request, *args, **kwargs):
        category = self.get_object()
        sub_categories = category.sub_categories.all()
        subcategory_serializer = CategorySerializer(sub_categories, many=True)
        data = subcategory_serializer.data
        return Response(data)

