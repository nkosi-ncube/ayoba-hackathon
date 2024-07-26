from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Customer, Order, Invoice, Payment, Query, Admin,OrderItem,BusinessProfile,Message,Testing
from .serializers import ProductSerializer, CustomerSerializer, OrderSerializer, InvoiceSerializer, PaymentSerializer, QuerySerializer, AdminSerializer,OrderItemSerializer,BusinessProfileSerializer,MessageSerializer,TestingSerializer
from django.views.decorators.csrf import csrf_exempt
from .services import send_message, send_file_message, get_media_slots, get_avatar_slot,get_message
from django.conf import settings
from django.shortcuts import render
import requests
import time

# jwt_token = login_to_ayoba(username, password)
# jwt_token = login_to_ayoba(username, password)
access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjliNTIwMGU1M2JjMGU2NDczYzllMzIyZDMwYjA2Yjk0MjZmYzEyY2IiLCJqaWQiOiI5YjUyMDBlNTNiYzBlNjQ3M2M5ZTMyMmQzMGIwNmI5NDI2ZmMxMmNiQGF5b2JhLm1lIiwiZ3JvdXAiOiJidXNpbmVzcyIsIm1zaXNkbiI6bnVsbCwiaWF0IjoxNzIyMDAwMTc2LCJleHAiOjE3MjIwMDE5NzZ9.d753qPhUptD_bksH3jdEOma89jCicP0lxDfPTwfXlOE"

def home(request):
    return render(request, 'home.html')
# Function-based views
@csrf_exempt
@api_view(['GET'])
def catalog_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@csrf_exempt
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
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        # Assuming that the request data contains msisdns, message_type, and message_text
        msisdns =  ["+27648917936"]
        message_type =  'text'
        message_text =  'Hie Njabulo  am testing from the interface'

        if message_type == 'text':
            response = send_message(msisdns, message_type, message_text)
            print("This is the response that came through: " ,response)

            time.sleep(5)
            response = get_message(msisdns, message_type, message_text)
        elif message_type == 'file':
            file_url = request.data.get('file_url', '')
            response = send_file_message(msisdns, file_url)
        else:
            return Response({"error": "Unsupported message type"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(response, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        # Fetching a message's details
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        # Retrieving messages sent from Ayoba users
        url = f"https://api.ayoba.me/v1/business/message"
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            messages = response.json()
            return Response(messages, status=status.HTTP_200_OK)
        except requests.exceptions.HTTPError as http_err:
            return Response({"error": f"HTTP error occurred: {http_err}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({"error": f"Other error occurred: {err}"}, status=status.HTTP_400_BAD_REQUEST)
# Class-based views
class BusinessProfileViewSet(viewsets.ModelViewSet):
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer

class TestingViewSet(viewsets.ModelViewSet):
    queryset = Testing.objects.all()
    serializer_class = TestingSerializer
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
# class MessageViewSet(viewsets.ModelViewSet):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class QueryViewSet(viewsets.ModelViewSet):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
