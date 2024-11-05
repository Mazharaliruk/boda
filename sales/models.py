from django.db import models

# Create your models here.

# Here are the choices for the order status
class OrderStatus(models.TextChoices):
    PENDING = 'P', 'Pending'
    COMPLETED = 'C', 'Completed'
    CANCELLED = 'X', 'Cancelled'
    REFUNDED = 'R', 'Refunded'
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
    CNY = 'CNY', 'CNY'
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
    CREDIT_CARD = 'CC', 'Credit Card'
    DEBIT_CARD = 'DC', 'Debit Card'
    BANK_TRANSFER = 'BT', 'Bank Transfer'
    CASH_ON_DELIVERY = 'COD', 'Cash On Delivery'
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
    transaction_fee = models.FloatField(null=True)
    additional_config = models.TextField(null=True)
    supported_currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.PKR)
    def __str__(self):
        return self.name

# 
    
    # Order Model 
class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.FloatField(null=True)
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.PKR)
    status = models.CharField(max_length=2, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    shipping_address = models.TextField(null=True)
    billing_address = models.TextField(null=True)
    discount_amount = models.FloatField(null=True)
    tax_amount = models.FloatField(null=True)
    note = models.TextField(null=True)
    def __str__(self):
        return self.status
    

# Transaction Model 
class Transaction(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.FloatField(null=True)
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.PKR)
    status = models.CharField(max_length=2, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_getway = models.ForeignKey(PaymentGetway, on_delete=models.CASCADE)
    transcation_date = models.DateTimeField(null=True)
    getway_response = models.JSONField(null=True)
    paymment_method = models.CharField(max_length=2, choices=PaymentMethod.choices, default=PaymentMethod.CREDIT_CARD)
    retry_count = models.IntegerField(null=True)
    def __str__(self):
        return self.status
    
    
#Payment Model 
class Payment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.FloatField(null=True)
    payment_date = models.DateTimeField(null=True)
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.PKR)
    status = models.CharField(max_length=2, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_getway = models.ForeignKey(PaymentGetway, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    paymment_method = models.CharField(max_length=2, choices=PaymentMethod.choices, default=PaymentMethod.CREDIT_CARD)
    transaction_refrence = models.CharField(null=True)
    refund_amount = models.FloatField(null=True)
    getway_response = models.JSONField(null=True)
    
    def __str__(self):
        return self.status