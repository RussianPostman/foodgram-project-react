from django.contrib import admin

from .models import (Follow, Tag, Ingredient, Recipe, IngredientToRecipe,
                     Favorite, ShoppingCart)


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )
    empty_value_display = '-пусто-'


class TegAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
        'image',
        'text',
        'cooking_time',
    )
    empty_value_display = '-пусто-'


class IngredientToRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient',
        'recipe',
        'amount',
    )
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    empty_value_display = '-пусто-'


admin.site.register(Follow, FollowAdmin)
admin.site.register(Tag, TegAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientToRecipe, IngredientToRecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
