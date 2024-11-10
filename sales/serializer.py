from rest_framework import serializers
from .models import  Order, Transaction, Payment, PaymentGetway



class PaymentGetwaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGetway
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
        
        
# Transaction Serializer
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        
# Payment Serializer
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        