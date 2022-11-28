from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import (Tag, Recipe, Ingredient,
                     IngredientToRecipe, ShoppingCart, Favorite)
from users.serializers import CustomUserSerializer


class TegSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientToRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all())
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientToRecipe
        fields = (
            'id',
            'amount',
            'name',
            'measurement_unit',
        )


class RecipeCreate(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True)
    ingredients = IngredientToRecipeSerializer(
        many=True,
        source='ingredienttorecipe')
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
                    ingredient = ingredient['id']
                    if not Ingredient.objects.filter(
                        id=ingredient.id
                    ).first():
                        raise serializers.ValidationError(
                            'Указанного ингредиента не существует')

        return data

    def create(self, validated_data):
        request = self.context.get('request', None)

        tags = validated_data.pop('tags')

        ingredients = validated_data.pop('ingredienttorecipe')

        current_user = request.user
        recipe = Recipe.objects.create(author=current_user, **validated_data)

        for tag in tags:
            recipe.tags.add(tag)

        for ingredient_data in ingredients:
            ingredient = ingredient_data.pop('id')
            amount = ingredient_data.pop('amount')
            ingredient = Ingredient.objects.get(id=ingredient.id)
            IngredientToRecipe.objects.create(
                ingredient=ingredient,
                amount=amount,
                recipe=recipe
            )
        return recipe

    def update(self, instance, validated_data):

        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredienttorecipe')

        instance.tags.clear()
        for tag in tags:
            instance.tags.add(tag)

        instance.ingredients.clear()
        for ingredient_data in ingredients:
            ingredient = ingredient_data.pop('id')
            amount = ingredient_data.pop('amount')
            ingredient = Ingredient.objects.get(id=ingredient.id)
            IngredientToRecipe.objects.create(
                ingredient=ingredient,
                amount=amount,
                recipe=instance
            )

        instance.image = validated_data.pop('image')
        instance.text = validated_data.pop('text')
        instance.cooking_time = validated_data.pop('cooking_time')
        instance.name = validated_data.pop('name')

        return instance
