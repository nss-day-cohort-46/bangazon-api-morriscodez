"""Module for expensive products report"""

from bangazonapi.views.product import ProductSerializer
import sqlite3
from django.shortcuts import render
from rest_framework.serializers import Serializer
from bangazonapi.models import Order
from bangazonreports.views import Connection

def completedorders_list(request):
    """Function to build html report of products above $1000"""

    order_list = Order.objects.filter(payment_type__isnull = False)

    
    template = 'orders/list_with_completed_orders.html'
    context = {
        'order_list': order_list
        }

    return render(request, template, context)