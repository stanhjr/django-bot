from rest_framework import serializers
from shops.models import City, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address_name', 'google_map_link']


class CitySerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)

    class Meta:
        model = City
        fields = ['name', 'addresses']
