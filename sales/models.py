from datetime import datetime
from django.db.models import Max
from django.db import models, transaction

# Create your models here.

# Here are the choices for the order status
class OrderStatus(models.TextChoices):
    PENDING = 'PENDING', 'PENDING'
    COMPLETED = 'COMPLETED', 'COMPLETED'
    CANCELLED = 'CANCELLED', 'CANCELLED'
    REFUNDED = 'REFUNDED', 'REFUNDED'
    def __str__(self):
        return self.value

class PaymentStatus(models.TextChoices):
    PAID = 'PAID', 'PAID'
    UNPAID = 'UNPAID', 'UNPAID'
 
    def __str__(self):
        return self.value
    
    
class TransactionStatus(models.TextChoices):
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    REFUNDED = 'REFUNDED'
    def __str__(self):
        return self.value
    

# Here are the choices for the currency
class Currency(models.TextChoices):
    INR = 'INR', 'INR'
    USD = 'USD', 'USD'
    EUR = 'EUR', 'EUR'
    GBP = 'GBP', 'GBP'
    AUD = 'AUD', 'AUD'
    CAD = 'CAD', 'CAD'
    JPY = 'JPY', 'JPY'
    RUB = 'RUB', 'RUB'
    KRW = 'KRW', 'KRW'
    CHF = 'CHF', 'CHF'
    BRL = 'BRL', 'BRL'
    CNY = 'CNY', 'CNY'
    HKD = 'HKD', 'HKD'
    MXN = 'MXN', 'MXN'
    NZD = 'NZD', 'NZD'
    PHP = 'PHP', 'PHP'
    SGD = 'SGD', 'SGD'
    THB = 'THB', 'THB'
    TRY = 'TRY', 'TRY'
    VND = 'VND', 'VND'
    ZAR = 'ZAR', 'ZAR'
    PKR = 'PKR', 'PKR'
    AED = 'AED', 'AED'
    def __str__(self):
        return self.value
    
# Payment Method Choices
class PaymentMethod(models.TextChoices):
    CREDIT_CARD = 'CREDIT_CARD', 'Credit Card'
    DEBIT_CARD = 'DEBIT_CARD', 'Debit Card'
    BANK_TRANSFER = 'BANK_TRANSFER', 'Bank Transfer'
    CASH_ON_DELIVERY = 'CASH_ON_DELIVERY', 'Cash On Delivery'
    def __str__(self):
        return self.value


    
#  Payment Getway
class PaymentGetway(models.Model):
    name = models.CharField(max_length=100)
    api_key = models.TextField(null=True)
    secret_key = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    base_url = models.URLField(null=True)
    status = models.BooleanField(default=False)
    transaction_fee = models.FloatField(null=True, blank=True)
    additional_config = models.TextField(null=True, blank=True)
    supported_currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.PKR)
    def __str__(self):
        return self.name

# 
    
    # Order Model 
class Order(models.Model):
    order_id = models.CharField(max_length=20, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.FloatField(default=0.0)
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.PKR)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    customer_id = models.ForeignKey('account.CustomerProfile', on_delete=models.CASCADE)
    vendor_id = models.ForeignKey('account.VendorProfile', on_delete=models.CASCADE)
    service = models.ForeignKey('core.Service', on_delete=models.CASCADE)
    event = models.ForeignKey('core.Event', on_delete=models.CASCADE)
    order_date = models.DateTimeField(null=True, blank=True)
    shipping_address = models.TextField(null=True, blank=True)
    billing_address = models.TextField(null=True, blank=True)
    discount_amount = models.FloatField(default=0.0)
    tax_amount = models.FloatField(default=0.0)
    note = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            today = datetime.now().strftime('%Y%m%d')
            with transaction.atomic():
                max_id = Order.objects.filter(order_id__startswith=f"ORD-{today}").aggregate(
                    max_id=Max('order_id')
                )['max_id']
                next_id = int(max_id.split('-')[-1]) + 1 if max_id else 1
                self.order_id = f"ORD-{today}-{next_id:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"order_id:{self.order_id} , status:{self.status} , id:{self.id}"
    

# Transaction Model 
class Transaction(models.Model):
    transaction_id = models.CharField(max_length=30, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.FloatField(null=True, blank=True, default=0.0)
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.PKR)
    status = models.CharField(max_length=20, choices=TransactionStatus.choices, default=TransactionStatus.SUCCESS)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_getway = models.ForeignKey(PaymentGetway, on_delete=models.CASCADE)
    transcation_date = models.DateTimeField(null=True, blank=True)
    getway_response = models.JSONField(null=True, blank=True)
    paymment_method = models.CharField(max_length=100, choices=PaymentMethod.choices, default=PaymentMethod.CREDIT_CARD)
    retry_count = models.IntegerField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            count = Transaction.objects.filter(order=self.order).count() + 1
            self.transaction_id = f"TXN-{self.order.order_id}-{count:02d}"
        super().save(*args, **kwargs)
    def __str__(self):
        return self.status
    
    
#Payment Model 
class Payment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.FloatField(null=True, blank=True, default=0.0)
    payment_date = models.DateTimeField(null=True, blank=True)
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.PKR)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_getway = models.ForeignKey(PaymentGetway, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    paymment_method = models.CharField(max_length=100,choices=PaymentMethod.choices, default=PaymentMethod.CREDIT_CARD)
    transaction_refrence = models.CharField(max_length=200,null=True, blank=True)
    refund_amount = models.FloatField(null=True, blank=True, default=0.0)
    getway_response = models.JSONField(null=True, blank=True)
    

    def __str__(self):
        return self.status