from django.core.paginator import Paginator, PageNotAnInteger
from rest_framework import serializers

from categories.models import Category
from products.serializers import ProductSerializer

PAGE_SIZE = 5


class CategoryNameSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count', 'count_parents']

    def get_products_count(self, obj):
        return obj.get_all_products_count()


class CategorySaleOutCategoryNameSerializer(CategoryNameSerializer):
    def get_products_count(self, obj):
        return obj.get_all_sale_out_products_count()


class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    sub_categories = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()
    total_pages = serializers.SerializerMethodField()
    next_page = serializers.SerializerMethodField()
    previous_page = serializers.SerializerMethodField()
    current_page = serializers.SerializerMethodField()
    parent_name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products', 'sub_categories',
                  'products_count', 'count_parents', 'parent_category_for_bot',
                  'parent', 'total_pages', 'next_page', 'previous_page', 'current_page', 'parent_name']

    def get_parent_name(self, obj):
        if hasattr(obj, 'parent'):
            return obj.parent.name

    def get_products(self, obj):
        paginator = Paginator(obj.products.all(), PAGE_SIZE)
        page = self.context['request'].query_params.get('page') or 1
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        serializer = ProductSerializer(pages, many=True)
        return serializer.data

    def get_sub_categories(self, obj):
        sub_categories = obj.sub_categories.all()
        serializer = CategoryNameSerializer(sub_categories, many=True)
        return serializer.data

    def get_products_count(self, obj):
        return obj.get_all_products_count()

    def get_total_pages(self, obj):
        paginator = Paginator(obj.products.all(), PAGE_SIZE)
        return paginator.num_pages

    def get_next_page(self, obj):
        request = self.context['request']
        paginator = Paginator(obj.products.all(), PAGE_SIZE)
        page = request.query_params.get('page') or 1
        if int(page) < paginator.num_pages:
            return int(page) + 1
        return None

    def get_previous_page(self, obj):
        request = self.context['request']
        page = request.query_params.get('page') or 1
        if int(page) > 1:
            return int(page) - 1
        return None

    def get_current_page(self, obj):
        request = self.context['request']
        page = request.query_params.get('page') or 1
        return int(page)


class CategorySaleOutSerializer(CategorySerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'products', 'sub_categories',
                  'products_count', 'count_parents', 'parent_category_for_bot',
                  'parent', 'total_pages', 'next_page', 'previous_page', 'current_page', 'parent_name']

    def get_products(self, obj):
        paginator = Paginator(obj.products.filter(sale_out=True).all(), PAGE_SIZE)
        page = self.context['request'].query_params.get('page') or 1
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        serializer = ProductSerializer(pages, many=True)
        return serializer.data

    def get_sub_categories(self, obj):
        sub_categories = obj.sub_categories.all()
        serializer = CategorySaleOutCategoryNameSerializer(sub_categories, many=True)
        return serializer.data

    def get_products_count(self, obj):
        return obj.get_all_sale_out_products_count()

    def get_total_pages(self, obj):
        paginator = Paginator(obj.products.filter(sale_out=True).all(), PAGE_SIZE)
        return paginator.num_pages

    def get_next_page(self, obj):
        request = self.context['request']
        paginator = Paginator(obj.products.filter(sale_out=True).all(), PAGE_SIZE)
        page = request.query_params.get('page') or 1
        if int(page) < paginator.num_pages:
            return int(page) + 1
        return None


