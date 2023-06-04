from rest_framework import viewsets
from rest_framework.response import Response

from categories.models import Category, SubCategory
from categories.serializers import CategorySerializer, SubCategorySerializer
from products.models import Product
from products.serializers import ProductSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        category = self.get_object()
        subcategories = SubCategory.objects.filter(category=category)
        subcategory_serializer = SubCategorySerializer(subcategories, many=True)
        data = subcategory_serializer.data
        return Response(data)


class SubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def retrieve(self, request, *args, **kwargs):
        sub_category = self.get_object()
        products = Product.objects.filter(sub_category=sub_category).exclude(status='sold')
        product_serializer = ProductSerializer(products, many=True)
        data = product_serializer.data
        return Response(data)
