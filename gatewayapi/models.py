from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class BusinessProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='business_profile')
    business_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    working_hours = models.TextField(blank=True, null=True)  # E.g., "Mon-Fri: 9 AM - 5 PM"
    description = models.TextField(blank=True, null=True)  # Additional details about the business

    def __str__(self):
        return self.business_name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    

class Customer(models.Model):
    name = models.CharField(max_length=255)
    language = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} for {self.customer.name}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    

class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    payment_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Invoice {self.id} for {self.order.customer.name}"
    

class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    payment_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment {self.id} for {self.invoice.order.customer.name}"
    

class Query(models.Model):  
    message = models.TextField()

    def __str__(self):
        return f"Query {self.id}"
    
class Admin(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    permissions = models.JSONField(default=dict)

    def __str__(self):
        return f"Admin {self.username}"
