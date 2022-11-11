from django_filters import FilterSet, DateTimeFilter
from .models import Post
from django.forms import DateTimeInput
import django_filters

class PostFilter(FilterSet):

    class Meta:
       model = Post
       fields = {
           # поиск по названию
           'title': ['icontains'],
           # количество товаров должно быть больше или равно
           'dateCreation': ['gte'],
           # 'dateCreationMore': ['gte'],
           'postCategory': ['exact'],
       }

       dateCreationMore = DateTimeFilter(
           field_name='dateCreation',
           lookup_expr='gte',
           widget=DateTimeInput(
               format='%Y-%m-%dT%H:%M',
               attrs={'type': 'datetime-local'},
           ),
       )