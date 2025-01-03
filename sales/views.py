from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order, Transaction, Payment, PaymentGetway
from .serializer import OrderSerializer, TransactionSerializer, PaymentGetwaySerializer,PaymentSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    @action(detail=False, methods=['get'], url_path='by-event')
    def get_orders_by_event(self, request):
        event = request.query_params.get('event')
        if not event:
            return Response({'error': 'event query parameter is required.'}, status=400)
        orders = Order.objects.filter(event=event)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-event-status')
    def get_orders_by_event_status(self, request):
        event = request.query_params.get('event')
        status = request.query_params.get('status')

        if not event:
            return Response({'error': 'event_id query parameter is required.'}, status=400)

        if not status:
            return Response({'error': 'status query parameter is required.'}, status=400)

        orders = Order.objects.filter(event_id=event, status=status)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)



class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
    
    

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
    
    
class PaymentGetwayViewSet(viewsets.ModelViewSet):
    queryset = PaymentGetway.objects.all()
    serializer_class = PaymentGetwaySerializer
    

