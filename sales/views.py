from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializer import OrderSerializer

@api_view(['GET'])
def orders(request):
    # Start with all orders
    orders = Order.objects.all()

    # Filter by order status (PENDING, COMPLETED, CANCELLED, REFUNDED)
    status_filter = request.query_params.get('status', None)
    if status_filter:
        orders = orders.filter(status=status_filter)

    # Filter by currency (e.g., INR, USD, EUR, etc.)
    currency_filter = request.query_params.get('currency', None)
    if currency_filter:
        orders = orders.filter(currency=currency_filter)

    # Filter by total_amount (greater than, less than, or exact match)
    min_amount = request.query_params.get('min_amount', None)
    if min_amount:
        orders = orders.filter(total_amount__gte=float(min_amount))

    max_amount = request.query_params.get('max_amount', None)
    if max_amount:
        orders = orders.filter(total_amount__lte=float(max_amount))

    # Filter by discount_amount (greater than, less than, or exact match)
    min_discount = request.query_params.get('min_discount', None)
    if min_discount:
        orders = orders.filter(discount_amount__gte=float(min_discount))

    max_discount = request.query_params.get('max_discount', None)
    if max_discount:
        orders = orders.filter(discount_amount__lte=float(max_discount))

    # Filter by tax_amount (greater than, less than, or exact match)
    min_tax = request.query_params.get('min_tax', None)
    if min_tax:
        orders = orders.filter(tax_amount__gte=float(min_tax))

    max_tax = request.query_params.get('max_tax', None)
    if max_tax:
        orders = orders.filter(tax_amount__lte=float(max_tax))

    # Filter by created_at date (range filters)
    date_created_from = request.query_params.get('date_created_from', None)
    if date_created_from:
        orders = orders.filter(created_at__gte=date_created_from)

    date_created_to = request.query_params.get('date_created_to', None)
    if date_created_to:
        orders = orders.filter(created_at__lte=date_created_to)

    # Filter by updated_at date (range filters)
    date_updated_from = request.query_params.get('date_updated_from', None)
    if date_updated_from:
        orders = orders.filter(updated_at__gte=date_updated_from)

    date_updated_to = request.query_params.get('date_updated_to', None)
    if date_updated_to:
        orders = orders.filter(updated_at__lte=date_updated_to)

    # Filter by shipping_address or billing_address (partial match)
    shipping_address = request.query_params.get('shipping_address', None)
    if shipping_address:
        orders = orders.filter(shipping_address__icontains=shipping_address)

    billing_address = request.query_params.get('billing_address', None)
    if billing_address:
        orders = orders.filter(billing_address__icontains=billing_address)

    # Filter by note (partial match)
    note = request.query_params.get('note', None)
    if note:
        orders = orders.filter(note__icontains=note)

    # Ordering the results
    order_by = request.query_params.get('order_by', None)
    if order_by:
        # Assuming order_by is a valid field in the Order model
        orders = orders.order_by(order_by)

    # Serialize the filtered and ordered orders
    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
