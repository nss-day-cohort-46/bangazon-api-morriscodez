from django.urls import path
from .views import expensiveproducts_list, inexpensiveproducts_list, completedorders_list

urlpatterns = [
    path('reports/expensiveproducts', expensiveproducts_list),
    path('reports/inexpensiveproducts', inexpensiveproducts_list),
    path('reports/completedorders', completedorders_list)
]
