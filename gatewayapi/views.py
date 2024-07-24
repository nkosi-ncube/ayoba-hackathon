from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Customer, Order, Invoice, Payment, Query, Admin,OrderItem,BusinessProfile
from .serializers import ProductSerializer, CustomerSerializer, OrderSerializer, InvoiceSerializer, PaymentSerializer, QuerySerializer, AdminSerializer,OrderItemSerializer,BusinessProfileSerializer
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
# Function-based views
@api_view(['GET'])
def catalog_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_to_cart(request):
    customer_id = request.data.get('customer_id')
    product_quantities = request.data.get('product_quantities', [])
    
    try:
        customer = Customer.objects.get(id=customer_id)
        
        total = 0
        order = Order.objects.create(customer=customer, total=0)
        
        for pq in product_quantities:
            product = Product.objects.get(id=pq['product_id'])
            quantity = pq['quantity']
            price = product.price * quantity
            total += price
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
        
        order.total = total
        order.save()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def checkout(request):
    order_id = request.data.get('order_id')
    
    try:
        order = Order.objects.get(id=order_id)
        invoice = Invoice.objects.create(order=order, status='Pending')
        payment = Payment.objects.create(invoice=invoice, status='Unpaid', amount=order.total)
        
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Class-based views
class BusinessProfileViewSet(viewsets.ModelViewSet):
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class QueryViewSet(viewsets.ModelViewSet):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer