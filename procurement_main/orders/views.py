from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Order, OrderItem, Contact
from .serializers import ContactSerializer, OrderSerializer, AddToCartSerializer
from drf_spectacular.utils import extend_schema
from products.models import ProductInfo
from core.tasks import send_order_email

class AddToCart(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddToCartSerializer

    @extend_schema(
        request=AddToCartSerializer,
        responses={200: AddToCartSerializer},
    )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        order, _ = Order.objects.get_or_create(
            user=request.user,
            status="basket"
        )

        product = ProductInfo.objects.get(
            id=serializer.validated_data["product_id"]
        )

        OrderItem.objects.create(
            order=order,
            product_info=product,
            quantity=serializer.validated_data["quantity"]
        )

        return Response({"message": "Товар добавлен"})


class RemoveFromCart(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)
        order_item.delete()
        return Response({"message": "Удалено"})


class ContactCreate(CreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ConfirmOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order = get_object_or_404(
            Order,
            id=request.data["order_id"],
            user=request.user
        )

        contact = get_object_or_404(
            Contact,
            id=request.data["contact_id"],
            user=request.user
        )

        order.contact = contact
        order.status = "new"
        order.save()
        send_order_email.delay(order.id, request.user.email)

        return Response({"message": "Заказ подтверждён"})


class OrderHistory(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).exclude(status="basket")