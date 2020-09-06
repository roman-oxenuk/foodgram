from django.contrib import admin

from .models import IngredientUnit, Ingredient, Recipe, IncludedInRecipe, Tag



class IncludedInRecipeInline(admin.TabularInline):
    model = IncludedInRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IncludedInRecipeInline,
    ]


admin.site.register(IngredientUnit)
admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
