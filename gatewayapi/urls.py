from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, CustomerViewSet, OrderViewSet, InvoiceViewSet, PaymentViewSet, 
    QueryViewSet, AdminViewSet, OrderItemViewSet, BusinessProfileViewSet, 
    catalog_list, add_to_cart, checkout, home, MessageViewSet
)

from django.conf import settings
from django.conf.urls.static import static

# Create a router and register viewsets with it
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'queries', QueryViewSet)
router.register(r'admins', AdminViewSet)
router.register(r'orderitems', OrderItemViewSet) 
router.register(r'businessprofiles', BusinessProfileViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', home, name='home'),  # Home view should come first
    path('catalog/', catalog_list, name='catalog-list'),  # Function-based view for catalog
    path('cart/', add_to_cart, name='add-to-cart'),  # Function-based view for adding items to the cart
    path('checkout/', checkout, name='checkout'),  # Function-based view for checkout
    path('api/', include(router.urls)),  # Use a prefix for API endpoints
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urls.py


