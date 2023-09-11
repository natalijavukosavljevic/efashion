from rest_framework import pagination
from rest_framework import filters
from django.db.models import Q
from store.models import Product

class CustomPagination(pagination.PageNumberPagination):
    
    page_size = len(Product.objects.all())
    page_size_query_param = 'page_size'
    max_page_size = len(Product.objects.all())
    page_query_param = 'p'


