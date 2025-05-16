from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models



class Users(AbstractUser):
    # username = models.CharField(max_length=100)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        related_query_name='user',
    )
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
    )
    email = models.EmailField()
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='manager')
    phone_number = models.CharField(max_length=20)
    # is_active = models.BooleanField(default=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Customers(models.Model):
    name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    color = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Orders(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='orders')
    ordered_thing = models.CharField(max_length=255, default='T-shirt')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    quantity = models.IntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_date = models.DateTimeField(null=True, blank=True)


class OrderItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product_items')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Inventory(models.Model):
    product = models.OneToOneField(Products, on_delete=models.CASCADE, related_name='inventory')
    quantity_in_stock = models.IntegerField()
    quantity_reserved = models.IntegerField()
    reorder_level = models.IntegerField()

    def __str__(self):
        return self.product.name


class Shipments(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='shipments')
    ship_date = models.DateTimeField(auto_now_add=True)
    courier_name = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=100)
    shipment_status = models.CharField(max_length=100)
    delivery_address = models.CharField(max_length=255)

    def __str__(self):
        return f"Shipment for {self.order.id}"


class Payments(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    payment_method = models.CharField(max_length=100)
    status = models.CharField(max_length=100)




