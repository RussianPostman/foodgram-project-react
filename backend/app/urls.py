from django.urls import include, path
from rest_framework import routers

from .views import TagViewSet, RecipeWiewSet, ShoppingCartMixin,\
     FavoriteMixin, IngredientMixin


router_v1 = routers.DefaultRouter()
router_v1.register('tags', TagViewSet)
router_v1.register('recipes', RecipeWiewSet)
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    ShoppingCartMixin,
    basename='shopping_cart')
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/favorite',
    FavoriteMixin,
    basename='favorite')
router_v1.register(
    'ingredients',
    IngredientMixin,
    basename='ingredients')

urlpatterns = [
    path('', include(router_v1.urls)),
]
