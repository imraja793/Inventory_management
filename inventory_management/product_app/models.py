from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=50, unique=True)

    class Meta:
        """Meta."""

        managed = True
        db_table = "location"

    def __str__(self):
        """__str__."""
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    product_id = models.CharField(max_length=50, unique=True)
    price = models.BigIntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    actual_quantity = models.IntegerField()
    product_record = JSONField(null=True)

    class Meta:
        """Meta."""

        managed = True
        db_table = "product"

    def __str__(self):
        """__str__."""
        return self.name



class WarehouseProductDescription(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    class Meta:
        """Meta."""

        managed = True
        db_table = "warehouseproductdescription"

    def __str__(self):
        """__str__."""
        return self.product.name


#
# class TrackProduct(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.CharField(max_length=10, default='1')
#     start_date = models.DateTimeField(auto_now_add=True)
#     end_date = models.DateTimeField(auto_now=True)
#     track = JSONField(null=True, blank=True)
#
#     class Meta:
#         """Meta."""
#
#         managed = True
#         db_table = "transport"
#
#     def __str__(self):
#         """__str__."""
#         return self.product.name