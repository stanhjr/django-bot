from rest_framework import serializers
from categories.models import Category
from products.serializers import ProductSerializer


class CategoryNameSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, obj):
        return obj.get_all_products_count()


class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    sub_categories = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products', 'sub_categories', 'products_count']

    def get_products(self, obj):
        products = obj.products.all()
        serializer = ProductSerializer(products, many=True)
        return serializer.data

    def get_sub_categories(self, obj):
        sub_categories = obj.sub_categories.all()
        serializer = CategoryNameSerializer(sub_categories, many=True)
        return serializer.data

    def get_products_count(self, obj):
        return obj.get_all_products_count()