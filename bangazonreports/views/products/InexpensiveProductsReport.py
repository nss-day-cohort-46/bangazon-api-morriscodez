"""Module for inexpensive products report"""

from bangazonapi.views.product import ProductSerializer
import sqlite3
from django.shortcuts import render
from rest_framework.serializers import Serializer
from bangazonapi.models import Product
from bangazonreports.views import Connection

def inexpensiveproducts_list(request):
    """Function to build html report of products below $1000"""

    product_list = Product.objects.filter(price__lte = 999)

    
    template = 'products/list_with_inexpensive_products.html'
    context = {
        'product_list': product_list
        }

    return render(request, template, context)