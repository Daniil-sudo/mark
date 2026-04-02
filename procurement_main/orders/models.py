from django.db import models
from django.conf import settings
from products.models import ProductInfo
from typing import Any


class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=50)
    corpus = models.CharField(max_length=50, blank=True)
    building = models.CharField(max_length=50, blank=True)
    apartment = models.CharField(max_length=50, blank=True)


class Order(models.Model):


    STATUS = [
        ("basket", "Корзина"),
        ("new", "Новый"),
        ("confirmed", "Подтвержден"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS, default="basket")
    contact = models.ForeignKey(Contact, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def total_price(self):
        return self.quantity * self.product_info.price