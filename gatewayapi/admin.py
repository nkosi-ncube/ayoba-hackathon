from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Customer, Order, Invoice, Payment, Query, Admin,BusinessProfile,Testing,Message
from django.utils.html import format_html


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'msisdn', 'message_id', 'from_jid', 'message_type', 'text', 'url', 'timestamp')
    search_fields = ('msisdn', 'message_id', 'from_jid', 'message_type')
    list_filter = ('message_type', 'timestamp')
    ordering = ('-timestamp',)
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'status', 'get_payment_status')

    def get_payment_status(self, obj):
        payment = Payment.objects.filter(invoice=obj).first()
        if payment:
            return format_html('<a href="{}">{}</a>', payment.get_absolute_url(), payment.status)
        return 'No payment'
    get_payment_status.short_description = 'Payment Status'
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price','image_url')
    search_fields = ('name',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'language')
    search_fields = ('name',)

@admin.register(Testing)
class TestingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total')
    search_fields = ('customer__name',)

# @admin.register(Invoice)
# class InvoiceAdmin(admin.ModelAdmin):
#     list_display = ('id', 'order', 'status', 'payment')
#     search_fields = ('order__id', 'status')
@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'contact_email', 'contact_phone', 'address', 'working_hours')
    search_fields = ('business_name', 'contact_email')
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'status', 'amount')
    search_fields = ('invoice__id', 'status')

@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'message')
    search_fields = ('message',)

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'permissions')
    search_fields = ('permissions',)
