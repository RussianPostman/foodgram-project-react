from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import (Tag, Recipe, Ingredient,
                     IngredientToRecipe, ShoppingCart, Favorite)
from users.serializers import CustomUserSerializer


class TegSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientToRecipeCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)
    amount = serializers.IntegerField(min_value=1)


# class IngredientSerializer(serializers.ModelSerializer):
#     amount = serializers.SerializerMethodField()

#     class Meta:
#         model = Ingredient
#         fields = ('id', 'name', 'measurement_unit', 'amount')

#     def get_amount(self, obj):
#         return obj.ingredient_to.amount


# class RecipeCreate(serializers.ModelSerializer):
#     image = Base64ImageField()
#     tags = serializers.PrimaryKeyRelatedField(
#         queryset=Tag.objects.all(),
#         many=True)
#     ingredients = IngredientToRecipeCreateSerializer(many=True)

#     class Meta:
#         model = Recipe
#         fields = (
#             'tags',
#             'ingredients',
#             'name',
#             'image',
#             'text',
#             'cooking_time',
#         )

#         extra_kwargs = {
#                 'ingredients': {'write_only': True}
#             }

#     def validate(self, data):
#         request = self.context.get('request', None)

#         # print('data!!!!!!!!!!')
#         # print(data)

#         if request.method == 'POST':
#             if 'tags' in data:
#                 tags = data['tags']
#                 for tag in tags:
#                     if not Tag.objects.filter(id=tag.id).first():
#                         raise serializers.ValidationError(
#                             'Указанного тега не существует')

#             if 'ingredients' in data:
#                 ingredients = data['ingredients']
#                 for ingredient in ingredients:
#                     print(ingredient)
#                     if not Ingredient.objects.filter(
#                         id=ingredient.get('id')
#                     ).first():
#                         raise serializers.ValidationError(
#                             'Указанного ингредиента не существует')

#         return data

#     def create(self, validated_data):
#         request = self.context.get('request', None)

#         tags = validated_data.pop('tags')
#         ingredients = validated_data.pop('ingredients')
#         current_user = request.user
#         recipe = Recipe.objects.create(author=current_user, **validated_data)

#         for tag in tags:
#             # tag = Tag.objects.get(id=tag.id)
#             recipe.tags.add(tag)

#         for ingredient in ingredients:
#             ingredient_id = ingredient.pop('id')
#             amount = ingredient.pop('amount')
#             ingredient = Ingredient.objects.get(id=ingredient_id)
#             print('!!!!CREATE!!!')
#             IngredientToRecipe.objects.create(
#                 ingredient=ingredient,
#                 amount=amount,
#                 recipe=recipe
#             )
#             print(str(recipe))
#         return recipe


class RecipeCreate(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True)
    ingredients = IngredientToRecipeCreateSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
    read_only_fields = ('id', 'author', 'is_favorited',
                        'is_favorited')

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request', None)
        if request:
            current_user = request.user
        if ShoppingCart.objects.filter(
            user=current_user.id,
            recipe=obj.id,
        ).exists():
            return True
        return False

    def get_is_favorited(self, obj):
        request = self.context.get('request', None)
        if request:
            current_user = request.user
        if Favorite.objects.filter(
            user=current_user.id,
            recipe=obj.id
        ).exists():
            return True
        return False

    def validate(self, data):
        request = self.context.get('request', None)

        # print('data!!!!!!!!!!')
        # print(data)

        if request.method == 'POST':
            if 'tags' in data:
                tags = data['tags']
                for tag in tags:
                    if not Tag.objects.filter(id=tag.id).first():
                        raise serializers.ValidationError(
                            'Указанного тега не существует')

            if 'ingredients' in data:
                ingredients = data['ingredients']
                for ingredient in ingredients:
                    print(ingredient)
                    if not Ingredient.objects.filter(
                        id=ingredient.get('id')
                    ).first():
                        raise serializers.ValidationError(
                            'Указанного ингредиента не существует')

        return data

    def create(self, validated_data):
        request = self.context.get('request', None)

        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        current_user = request.user
        recipe = Recipe.objects.create(author=current_user, **validated_data)

        for tag in tags:
            # tag = Tag.objects.get(id=tag.id)
            recipe.tags.add(tag)

        for ingredient in ingredients:
            ingredient_id = ingredient.pop('id')
            amount = ingredient.pop('amount')
            ingredient = Ingredient.objects.get(id=ingredient_id)
            print('!!!!CREATE!!!')
            IngredientToRecipe.objects.create(
                ingredient=ingredient,
                amount=amount,
                recipe=recipe
            )
            print(str(recipe))
        return recipe
