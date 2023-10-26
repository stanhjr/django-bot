from rest_framework import serializers
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('image_url', 'id', 'code', 'name', 'description', 'price', 'image', 'tg_nickname', 'phone')

    def get_name(self, obj):
        return obj.name.capitalize()

    def get_description(self, obj):
        return obj.description.capitalize()
