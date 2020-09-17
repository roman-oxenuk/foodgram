from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class IngredientUnit(models.Model):
    """Единица измерение игредиента (граммы, штуки, литры и т.д.)"""
    short_name = models.CharField('Короткое название', max_length=255)
    long_name = models.CharField('Длинное название', max_length=255)

    def __str__(self):
        return f'{self.short_name}. {self.long_name}'


class Ingredient(models.Model):
    """Ингредиент для рецепта """
    name = models.CharField('Название ингредиента', max_length=255)
    units = models.ForeignKey(IngredientUnit, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField('Тег', max_length=255)
    style = models.CharField('Префикс стиля для шаблона', max_length=255, null=True)
    human_name = models.CharField('Выводить в шаблоне имя', max_length=255, null=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Рецепт блюда """
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField('Название блюда', max_length=255)
    image = models.ImageField(upload_to='recipes', null=True)
    description = models.TextField('Описание блюда', null=True)
    tags = models.ManyToManyField(Tag, null=True)
    time_to_cook = models.IntegerField('Время приготовления', null=True)
    slug = models.SlugField(null=True)

    def __str__(self):
        return f'id: {self.pk}, {self.title}'

    @property
    def description_as_list(self):
        return self.description.split('\n')


class IncludedInRecipe(models.Model):
    """M2M-таблица, связывающая Рецепт и его Ингредиенты.

    Хранит кол-во ингредиента, нужного для приготовления блюда по Рецепту.
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.DecimalField('Количество', max_digits=6, decimal_places=2)
