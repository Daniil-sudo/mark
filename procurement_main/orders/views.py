from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Order, OrderItem, Contact
from .serializers import ContactSerializer, OrderSerializer
from products.models import ProductInfo


class AddToCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order, _ = Order.objects.get_or_create(user=request.user, status="basket")
        product = ProductInfo.objects.get(id=request.data["product_id"])
        OrderItem.objects.create(order=order, product_info=product, quantity=request.data["quantity"])
        return Response({"message": "Товар добавлен"})


class RemoveFromCart(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        OrderItem.objects.filter(id=item_id, order__user=request.user).delete()
        return Response({"message": "Удалено"})


class ContactCreate(CreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ConfirmOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order = Order.objects.get(id=request.data["order_id"], user=request.user)
        contact = Contact.objects.get(id=request.data["contact_id"])

        order.contact = contact
        order.status = "new"
        order.save()

        return Response({"message": "Заказ подтверждён"})


class OrderHistory(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).exclude(status="basket")