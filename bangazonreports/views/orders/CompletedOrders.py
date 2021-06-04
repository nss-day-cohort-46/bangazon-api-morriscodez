"""Module for expensive products report"""

from bangazonapi.views.product import ProductSerializer
import sqlite3
from django.shortcuts import render
from rest_framework.serializers import Serializer
from bangazonapi.models import Order, order
from bangazonreports.views import Connection


def SQLcompletedorders_list(request):
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory= sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT
                    o.*,
                    u.first_name || " " || u.last_name as "Customer_Name",
                    p.merchant_name,
                    SUM(pr.price) as "Total_Price"
                FROM
                    bangazonapi_order o
                JOIN
                    bangazonapi_payment p on o.payment_type_id = p.id
                JOIN
                    bangazonapi_customer c on o.customer_id = c.id
                JOIN 
                    auth_user u on c.user_id = u.id
                JOIN
                    bangazonapi_orderproduct op on o.id = op.order_id
                JOIN
                    bangazonapi_product pr on op.product_id = pr.id
                WHERE
                    o.payment_type_id is not NULL
                GROUP BY
                    op.order_id
            """)

            dataset = db_cursor.fetchall()

            completed_orders_list = []

            for row in dataset:
                # Create a Game instance and set its properties
                order = {}
                order["id"] = row["id"]
                order["created_date"] = row["created_date"]
                order["payment_type_id"] = row["payment_type_id"]
                order["merchant_name"] = row["merchant_name"]
                order["customer_name"] = row["Customer_Name"]
                order["total_price"] = row["Total_Price"]
                
                completed_orders_list.append(order)
                    
        
        # Get only the values from the dictionary and create a list from them
        list_of_completed_orders = completed_orders_list

        # Specific the Django template and provide data context
        template = 'orders/list_with_completed_orders.html'
        context = {
            'orders_list': list_of_completed_orders
        }

        return render(request, template, context)