from rest_framework import serializers
from .models import Contact, Order, OrderItem


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"
        read_only_fields = ("user",)


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(source="product_info.product")

    class Meta:
        model = OrderItem
        fields = ("product", "quantity", "total_price")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("id", "created_at", "status", "items", "total_amount")

    def get_total_amount(self, obj):
        return sum(i.total_price for i in obj.items.all())