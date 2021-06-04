"""Module for favorite sellers report"""

from bangazonapi.views.product import ProductSerializer
import sqlite3
from django.shortcuts import render
from rest_framework.serializers import Serializer
from bangazonapi.models import Customer, favorite
from bangazonreports.views import Connection


def favoritesellers_list(request):
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory= sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT
                    c.*,
                    u.first_name || " " || u.last_name as Customer_Name,
                    f.seller_id,
                    au.first_name || " " || au.last_name as Seller_Name
	
                FROM bangazonapi_customer c
                JOIN bangazonapi_favorite f on f.customer_id = c.id
                JOIN auth_user u on f.customer_id = u.id
                JOIN auth_user au on f.seller_id = au.id 
                ORDER BY f.customer_id
            """)

            dataset = db_cursor.fetchall()

            favorites_list = {}

            for row in dataset:
                # Create a Game instance and set its properties
                favorite = Customer()
                fid = row["id"]
                favorite.customer_name = row["Customer_Name"]
                favorite.favorite_sellers = row["Seller_Name"]
                
                if fid in favorites_list:
                    favorites_list[fid]["customer_name"]['favorite_sellers'].append(favorite.favorite_sellers)

                else:
                    favorites_list[fid] = {}
                    favorites_list[fid]["customer_name"] = row["Customer_Name"] 
                    favorites_list[fid]["customer_name"]["favorite_sellers"] = row["favorite_sellers"]

                    
        
        # Get only the values from the dictionary and create a list from them
        list_of_favorites = favorites_list.values()

        # Specific the Django template and provide data context
        template = 'users/favorite_sellers_list.html'
        context = {
            'favorites_list': list_of_favorites
        }

        return render(request, template, context)