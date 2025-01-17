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
from .tokenManager import token_manager
# jwt_token = login_to_ayoba(username, password)
# jwt_token = login_to_ayoba(username, password)
access_token= token = token_manager.get_token()

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
        print("Request data: ", request.data)
        msisdns =  request.data.get('msisdns', [])
        message_type =  request.data.get('message_type', '')
        message_text =  request.data.get('message_text', '')

        if message_type == 'text':
            response = send_message(msisdns, message_type, message_text)
            print("This is the response that came through: " ,response)

            # time.sleep(5)
            # response = get_message(msisdns, message_type, message_text)
            # if len(response) > 0:
            #     response = response[-1]["message"]["text"]
            # else:
            #     response = "No message received"
        elif message_type == 'file':
            file_url = request.data.get('file_url', '')
            response = send_file_message(msisdns, file_url)
        else:
            return Response({"error": "Unsupported message type"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(response, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        print("GET request received")
        # Ensure access_token is defined and valid
        print("Access token:", access_token)
        
        url = f"https://api.ayoba.me/v1/business/message"
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            messages = response.json()
            print("Messages fetched:", messages)
            return Response(messages, status=status.HTTP_200_OK)
        except requests.exceptions.HTTPError as http_err:
            print("HTTP error:", http_err)
            return Response({"error": f"HTTP error occurred: {http_err}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print("Other error:", err)
            return Response({"error": f"Other error occurred: {err}"}, status=status.HTTP_400_BAD_REQUEST)
import json
from django.http import JsonResponse
from .lelapa import translate_text
@csrf_exempt
def translate_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text')
            choice = data.get('choice')

            if not text or not choice:
                return JsonResponse({"error": "Both 'text' and 'choice' are required."}, status=400)

            translated_text = translate_text(text, choice)
            return JsonResponse({"translated_text": translated_text})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method is allowed."}, status=405)
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
