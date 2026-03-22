from rest_framework import serializers
from .models import Product, ProductInfo, ProductParameter


class ProductParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductParameter
        fields = ("key", "value")


class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = ("price", "quantity")


class ProductSerializer(serializers.ModelSerializer):
    supplier = serializers.StringRelatedField()
    parameters = ProductParameterSerializer(many=True)
    offers = ProductInfoSerializer(many=True)

    class Meta:
        model = Product
        fields = ("name", "description", "supplier", "parameters", "offers")