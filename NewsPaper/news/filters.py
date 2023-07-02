from django import forms
from django_filters import FilterSet, DateFilter, CharFilter
from .models import Post


class PostFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains', label='Заголовок')
    {'author':['icontains']}
    creation_date_time = DateFilter(field_name="creation_date_time", lookup_expr='gt', label='Дата создания', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = ['title', 'author', 'creation_date_time']