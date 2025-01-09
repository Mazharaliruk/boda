from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order, Transaction, Payment, PaymentGetway
from .serializer import OrderSerializer, TransactionSerializer, PaymentGetwaySerializer,PaymentSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    # get order by event
    @action(detail=False, methods=['get'], url_path='by-event')
    def get_orders_by_event(self, request):
        event = request.query_params.get('event')
        if not event:
            return Response({'error': 'event query parameter is required.'}, status=400)
        orders = Order.objects.filter(event=event)
        if not orders:
            return Response({'message': 'No orders found for the provided event.'}, status=404)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    # get order by event and status
    @action(detail=False, methods=['get'], url_path='by-event-status')
    def get_orders_by_event_status(self, request):
        event = request.query_params.get('event')
        status = request.query_params.get('status')

        if not event:
            return Response({'error': 'event_id query parameter is required.'}, status=400)

        if not status:
            return Response({'error': 'status query parameter is required.'}, status=400)

        orders = Order.objects.filter(event_id=event, status=status)
        if not orders:
            return Response({'message': 'No orders found for the provided event and status.'}, status=404)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    
    # get order by vendor
    @action(detail=False, methods=['get'], url_path='by-vendor')
    def get_orders_by_vendor(self, request):
        vendor = request.query_params.get('vendor')
        if not vendor:
            return Response({'error': 'vendor query parameter is required.'}, status=400)
        orders = Order.objects.filter(vendor_id=vendor)
        # if vendor does not match or available show message
        if not orders:
            return Response({'message': 'No orders found for the provided vendor.'}, status=404)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    # get order by vendor and status completed
    @action(detail=False, methods=['get'], url_path='by-vendor-status')
    def get_orders_by_vendor_status(self, request):
        vendor = request.query_params.get('vendor')
        status = request.query_params.get('status')

        if not vendor:
            return Response({'error': 'vendor_id query parameter is required.'}, status=400)

        if not status:
            return Response({'error': 'status query parameter is required.'}, status=400)

        orders = Order.objects.filter(vendor_id=vendor, status=status)
        if not orders:
            return Response({'message': 'No orders found for the provided vendor and status.'}, status=404)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)



class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
    # get transaction by order
    @action(detail=False, methods=['get'], url_path='by-order')
    def get_transactions_by_order(self, request):
        order = request.query_params.get('order')
        if not order:
            return Response({'error': 'order query parameter is required.'}, status=400)
        transactions = Transaction.objects.filter(order=order)
        if not transactions:
            return Response({'message': 'No transactions found for the provided order.'}, status=404)
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)
    
    
    

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
    
    
class PaymentGetwayViewSet(viewsets.ModelViewSet):
    queryset = PaymentGetway.objects.all()
    serializer_class = PaymentGetwaySerializer
    

