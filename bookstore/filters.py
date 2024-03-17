import django_filters
from .models import Books

class BookFilter(django_filters.FilterSet):
  book_name=django_filters.CharFilter(field_name='book_name', lookup_exp  ='icontains')
  
  class Meta:
    model = Books
    fields = ['book_name']
    
    