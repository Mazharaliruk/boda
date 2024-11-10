from django.db.models import Q
from rest_framework import viewsets
from .models import Order
from .serializer import OrderSerializer, TransactionSerializer, PaymentGetwaySerializer,PaymentSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer




class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = TransactionSerializer
    
    
    

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = PaymentSerializer
    
    
    
class PaymentGetwayViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = PaymentGetwaySerializer
    

