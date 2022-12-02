from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import (Tag, Recipe, Ingredient, Follow,
                     IngredientToRecipe, ShoppingCart, Favorite)
from users.serializers import CustomUserSerializer

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class ShortResipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(ShortResipeSerializer):

    def validate(self, data):
        request = self.context.get('request', None)
        current_recipe_id = self.context.get('request').parser_context.get(
            'kwargs').get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=current_recipe_id)

        if ShoppingCart.objects.filter(
            user=request.user,
            recipe=recipe
        ).first():
            raise serializers.ValidationError(
                'Рецепт уже в списке покупок')
        return data

    def create(self, validated_data):
        request = self.context.get('request', None)
        current_user = request.user
        current_recipe_id = self.context.get('request').parser_context.get(
            'kwargs').get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=current_recipe_id)
        ShoppingCart.objects.create(user=current_user, recipe=recipe)
        return recipe


class FavoriteSerializer(ShortResipeSerializer):

    def validate(self, data):
        request = self.context.get('request', None)
        current_recipe_id = self.context.get('request').parser_context.get(
            'kwargs').get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=current_recipe_id)

        if Favorite.objects.filter(
            user=request.user,
            recipe=recipe
        ).first():
            raise serializers.ValidationError(
                'Рецепт уже добавлен в избранное')
        return data

    def create(self, validated_data):
        request = self.context.get('request', None)
        current_user = request.user
        current_recipe_id = self.context.get('request').parser_context.get(
            'kwargs').get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=current_recipe_id)
        Favorite.objects.create(user=current_user, recipe=recipe)
        return recipe


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


class RecipeFollowSerializer(ShortResipeSerializer):
    def get_queryset(self):
        recipes_limit = self.context.get('request').parser_context.get(
            'kwargs').get('recipes_limit')
        print(recipes_limit)
        return Recipe.objects.all()


class FollowSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes'
        )
        read_only_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes'
        )

    def get_recipes(self, obj):
        limit = self.context.get('request').query_params.get('recipes_limit')
        if limit:
            queryset = Recipe.objects.filter(
                author=obj).order_by('-id')[:int(limit)]
        else:
            queryset = Recipe.objects.filter(author=obj)

        return ShortResipeSerializer(queryset, many=True).data

    def create(self, validated_data):
        request = self.context.get('request', None)
        author_id = self.context.get('request').parser_context.get(
            'kwargs').get('user_id')

        current_user = request.user
        author = get_object_or_404(User, pk=author_id)
        Follow.objects.create(user=current_user, author=author)
        return author
