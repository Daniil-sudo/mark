from rest_framework import serializers
from .models import Contact, Order, OrderItem
from django.db.models import Sum


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "phone",
            "city",
            "street",
            "house",
            "building",
            "apartment",
        )
        read_only_fields = ("id","user")


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(source="product_info.product")
    price = serializers.DecimalField(
        source="product_info.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    class Meta:
        model = OrderItem
        fields = ("id", "product", "price", "quantity", "total_price")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    contact = ContactSerializer(read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("id", "created_at", "status", "items","contact", "total_amount")

    def get_total_amount(self, obj):
        return obj.items.aggregate(total=Sum("total_price"))["total"] or 0

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)