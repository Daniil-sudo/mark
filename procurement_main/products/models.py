from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)


class ProductParameter(models.Model):
    product = models.ForeignKey(Product, related_name="parameters", on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, related_name="offers", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()