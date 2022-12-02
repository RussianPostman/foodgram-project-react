from django_filters import rest_framework
from rest_framework.filters import SearchFilter
import django_filters

from .models import Recipe, Tag, Ingredient


class IngredientFilter(SearchFilter):
    """Специальный фильтр для ингредиентов"""

    search_param = 'name'

    class Meta:
        model = Ingredient
        fields = ('name',)


class MyFilterSet(rest_framework.FilterSet):
    """Фильтр для Рецептов"""

    author = rest_framework.NumberFilter(field_name='author__id')
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
        )
    is_favorited = django_filters.NumberFilter(
        method='filter_is_favorited')
    is_in_shopping_cart = django_filters.NumberFilter(
        method='filter_shopping_cart')

    def filter_shopping_cart(self, qs, name, value):
        if value == 1:
            return qs.filter(shopping_list__user=self.request.user)

    def filter_is_favorited(self, qs, name, value):
        if value == 1:
            return qs.filter(favorites__user=self.request.user)

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']
