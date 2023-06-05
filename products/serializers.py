from rest_framework import serializers
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('image_url', 'id', 'code', 'name', 'description', 'price', 'image', 'tg_nickname', 'phone')
