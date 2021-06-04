"""Module for expensive products report"""

from bangazonapi.views.product import ProductSerializer
import sqlite3
from django.shortcuts import render
from rest_framework.serializers import Serializer
from bangazonapi.models import Order
from bangazonreports.views import Connection

def incompleteorders_list(request):
    """Function to build html report of products above $1000"""

    order_list = Order.objects.filter(payment_type__isnull = True)
    


    
    template = 'orders/list_with_incomplete_orders.html'
    context = {
        'order_list': order_list
        }

    return render(request, template, context)