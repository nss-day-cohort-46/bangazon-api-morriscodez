from django.urls import path
from .views import expensiveproducts_list

urlpatterns = [
    path('reports/expensiveproducts', expensiveproducts_list)
]
