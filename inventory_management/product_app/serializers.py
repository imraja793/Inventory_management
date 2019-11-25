from rest_framework import serializers

from product_app.models import Location, Product, WarehouseProductDescription


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class WarehouseProductDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseProductDescription
        fields = "__all__"
