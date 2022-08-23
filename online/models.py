from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import *

# Create your models here.
CATEGORY_CHOICES = (
    ('R', 'Ring'),
    ('B', 'Bracelet'),
    ('N', 'Necklace'),
)

REPORT_CHOICES = (
    ('P', 'Product'),
    ('S', 'Shipping'),
    ('O', 'Order'),
)


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.title)


class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=90, default="")
    phone = models.IntegerField(default="")
    message = models.CharField(max_length=6000, default="")

    def __str__(self):
        return str(self.name)


class ProductReport(models.Model):
    select_report = models.CharField(choices=REPORT_CHOICES, max_length=2, verbose_name="report")
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=90)
    user_email = models.EmailField(max_length=254)
    report_message = models.CharField(max_length=6000, default="")

    def __str__(self):
        return str(self.product_id)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.user)

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    Postcode = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On-Way', 'On-Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return str(self.user)

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price


class VerifiedEmail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=150)
    verify = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)
