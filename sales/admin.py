from django.contrib import admin
from sales.models import Order, Transaction, Payment, PaymentGetway



# Customize your model here.
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'order_id', 'created_at', 'updated_at', 'total_amount', 'currency', 'status',
        'shipping_address', 'billing_address', 'discount_amount', 'tax_amount', 'note', 'order_date',
        'customer_id', 'vendor_id', 'service', 'event',
    ]
    search_fields = ['currency']
        
    
    

class TransactionAdmin(admin.ModelAdmin):
   list_display = [
        'id', 'transaction_id', 'created_at', 'updated_at', 'amount', 'currency', 'status', 'order',
        'payment_getway', 'transcation_date', 'getway_response', 'paymment_method', 'retry_count'
    ]
   search_fields = ['currency','id']
   
   

class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'created_at', 'updated_at', 'amount', 'payment_date', 'currency', 'status', 
        'order', 'payment_getway', 'transaction', 'paymment_method', 'transaction_refrence', 
        'refund_amount', 'getway_response'
    ]
    search_fields = ['paymment_method', 'payment_getway__name', 'currency','id']
    list_filter = ['paymment_method', 'currency']
    

class PaymentGetwayAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'api_key', 'secret_key', 'created_at', 'updated_at', 'base_url', 
        'status', 'transaction_fee', 'additional_config', 'supported_currency'
    ]
    search_fields = ['supported_currency','name','id']
    list_filter = ['name', 'supported_currency']


# Register your models here.
admin.site.register(Order, OrderAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentGetway, PaymentGetwayAdmin)





