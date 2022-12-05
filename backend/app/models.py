from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from colorfield.fields import ColorField
from django.db.models import UniqueConstraint

from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    """ Модель тегов. """

    name = models.CharField(
        max_length=200,
        verbose_name='Название тега'
    )
    color = ColorField(
        verbose_name='Цвет',
        format='hex',
        max_length=7
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор тега типа slug'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    """ Модель ингредиентов. """

    name = models.CharField(
        max_length=200,
        verbose_name='Название продукта'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    """ Модель рецептов. """

    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientToRecipe',
        related_name='recipes',
        verbose_name='Ингредиент'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='app/',
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message='Не менее одной минуты'),
            MaxValueValidator(1440, message='Не долше 24 часов'),
        ],
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name} автор: {self.author.get_username()}'


class IngredientToRecipe(models.Model):
    """ Модель связки рецепта и ингредиента. """

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredienttorecipe'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message='Введите положительное число'),
        ],
    )

    class Meta:
        verbose_name = 'Связь рецепта и ингредиента'
        verbose_name_plural = 'Связи рецептов и ингредиентов'

    def __str__(self):
        return (f'Связь ингредиента {self.ingredient.name}'
                + f' и рецепта: {self.recipe.name}')


class Follow(models.Model):
    """ Модель подписки на автора. """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('user', 'author'),
                name='user_follow_unique'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return (f'Подписка {self.user.get_username}'
                + f' на: {self.author.get_username}')


class Favorite(models.Model):
    """ Модель добавление в избраное. """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorites',
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='user_favorite_unique'
            )
        ]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return (f'Избранный рецепт {self.recipe.name}'
                + f' пользователя: {self.user.get_username}')


class ShoppingCart(models.Model):
    """ Модель списка покупок. """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shopping_list',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='shopping_list',
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='user_shopping_unique'
            )
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

    # def __str__(self):
    #     return (f'Рецепт {self.recipe.name} в списке покупок',
    #             f' пользователя: {self.user.get_username}')
