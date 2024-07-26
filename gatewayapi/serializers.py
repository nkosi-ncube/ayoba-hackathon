from rest_framework import serializers
from .models import Product, Customer, Order, Invoice, Payment, Query, Admin,OrderItem,BusinessProfile,Message,Testing

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
class TestingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testing
        fields = '__all__'
class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = '__all__'
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price",'image_url']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "name", "language"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)  # Nested serializer for OrderItem

    class Meta:
        model = Order
        fields = ['id', 'customer', 'total', 'created_at', 'updated_at', 'items']



class InvoiceSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Invoice
        fields = ["id", "order", "status", "payment_id"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "invoice", "status", "payment_id", "amount"]


class QuerySerializer(serializers.ModelSerializer):  
    class Meta:
        model = Query
        fields = ["id", "message"]

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ["id", "username", "password", "permissions"]