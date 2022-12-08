from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import (Tag, Recipe, Ingredient, Follow,
                     IngredientToRecipe, ShoppingCart, Favorite)
from users.serializers import CustomUserSerializer

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TegSerializer(serializers.ModelSerializer):
    """Сериализатор тегов"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class ShortResipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов для простого короткого отображения"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(ShortResipeSerializer):
    """Сериализатор списка покупок"""

    def validate(self, data):
        request = self.context.get('request', None)
        current_recipe_id = self.context.get('request').parser_context.get(
            'kwargs').get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=current_recipe_id)

        if ShoppingCart.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists():
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
    """Сериализатор избранного"""

    def validate(self, data):
        request = self.context.get('request', None)
        current_recipe_id = self.context.get('request').parser_context.get(
            'kwargs').get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=current_recipe_id)

        if Favorite.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists():
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
    """Сериализатор модели соединяющей ингредиенты и рецепты"""

    id = serializers.IntegerField(
        source='ingredient.id'
    )
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


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор чтения рецептов"""

    tags = serializers.SerializerMethodField()
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

    def get_tags(self, obj):
        return TegSerializer(
            Tag.objects.filter(recipes=obj),
            many=True,).data

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request', None)
        if request:
            current_user = request.user
        return ShoppingCart.objects.filter(
            user=current_user.id,
            recipe=obj.id,
        ).exists()

    def get_is_favorited(self, obj):
        request = self.context.get('request', None)
        if request:
            current_user = request.user
        return Favorite.objects.filter(
            user=current_user.id,
            recipe=obj.id
        ).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания рецептов"""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True)
    ingredients = IngredientToRecipeSerializer(
        many=True,
        source='ingredienttorecipe')
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate(self, data):
        request = self.context.get('request', None)
        tags_list = []
        ingredients_list = []
        request_methods = ['POST', 'PATCH']

        if request.method in request_methods:
            if 'tags' in data:
                tags = data['tags']

                for tag in tags:
                    if tag.id in tags_list:
                        raise serializers.ValidationError(
                            F'Тег {tag} повторяется')
                    tags_list.append(tag.id)

                if len(tags_list) == 0:
                    raise serializers.ValidationError(
                            'Список тегов не должен быть пустым')

                all_tags = Tag.objects.all().values_list('id', flat=True)
                if not set(tags_list).issubset(all_tags):
                    raise serializers.ValidationError(
                        F'Тега {tag} не существует')

            if 'ingredienttorecipe' in data:
                ingredients = data['ingredienttorecipe']
                for ingredient in ingredients:
                    ingredient = ingredient['ingredient'].get('id')

                    if ingredient in ingredients_list:
                        raise serializers.ValidationError(
                            F'Ингредиент {ingredient} повторяется')
                    ingredients_list.append(ingredient)

                all_ingredients = Ingredient.objects.all().values_list(
                    'id', flat=True)

                if not set(ingredients_list).issubset(all_ingredients):
                    raise serializers.ValidationError(
                        'Указанного ингредиента не существует')

                if len(ingredients_list) == 0:
                    raise serializers.ValidationError(
                            'Список ингредиентов не должен быть пустым')
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
            ingredient = ingredient_data.pop('ingredient').get('id')
            amount = ingredient_data.pop('amount')
            ingredient = Ingredient.objects.get(id=ingredient)
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
            ingredient = ingredient_data.pop('ingredient').get('id')
            amount = ingredient_data.pop('amount')
            ingredient = Ingredient.objects.get(id=ingredient)
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

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context={
                 'request': self.context.get('request')
            }).data


class FollowSerializer(CustomUserSerializer):
    """Сериализатор ингредиентов"""

    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        read_only_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        limit = self.context.get('request').query_params.get('recipes_limit')
        if limit:
            queryset = Recipe.objects.filter(
                author=obj).order_by('-id')[:int(limit)]
        else:
            queryset = Recipe.objects.filter(author=obj)

        return ShortResipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def create(self, validated_data):
        request = self.context.get('request', None)
        author_id = self.context.get('request').parser_context.get(
            'kwargs').get('user_id')

        current_user = request.user
        author = get_object_or_404(User, pk=author_id)
        Follow.objects.create(user=current_user, author=author)
        return author
