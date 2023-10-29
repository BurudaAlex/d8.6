import django_filters
from django_filters import FilterSet, ModelMultipleChoiceFilter
from .models import Post
from django import forms

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    date = django_filters.DateFilter(
        field_name='time_in',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Date',
        lookup_expr='date'

    )
    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           'type': ['icontains'],
           # количество товаров должно быть больше или равно
           'author': ['gt'],
           'time_in':['gt']
       }