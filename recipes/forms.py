import re
from itertools import groupby

from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.core.exceptions import ValidationError

from .models import Tag, Recipe, Ingredient, IncludedInRecipe


class TagsFilterForm(forms.Form):

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=CheckboxSelectMultiple(),
        to_field_name='name'
    )


class RecipeCreateForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('title', 'tags')
         # 'tags')      # 'image', 'description', 'time_to_cook')
        # widgets = {
        #     'tags': CheckboxSelectMultiple(),
        # }

    def clean_title(self):
        title = self.cleaned_data['title']
        if title.lower() in ('create'):
            raise ValidationError(f'Недопустимое имя "{title}"')
        return title


class IncludedInRecipeForm(forms.ModelForm):

    in_recipe_id = forms.CharField(required=False, widget=forms.HiddenInput)
    ingredient = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.HiddenInput,
        required=False
    )
    name = forms.CharField(widget=forms.HiddenInput)
    amount = forms.CharField(widget=forms.HiddenInput)
    units = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = IncludedInRecipe
        fields = ('amount', 'ingredient')

    def save(self, commit=True):
        if not hasattr(self.instance, 'ingredient'):
            new_ingredient = Ingredient(
                name=self.cleaned_data['name'],
                units_id=Ingredient.DEFAULT_UNITS_PK
            )
            new_ingredient.save()
            self.instance.ingredient = new_ingredient
        super().save(commit)

    def clean_amount(self):
        amount = int(self.cleaned_data['amount'])
        if amount <= 0:
            raise ValidationError('Кол-во должно быть положительным числом')
        return amount


# TODO:
# * is_valid запускает валидацию всех форм
#     если определено parent_instance, то проверяем, принадлежат ли инстансы из форм этому parent_instance
#            если нет, то игнорим их
#
# * save запускает save у форм и добавляет parent_instance как recipe
#
# * если передан initial, то передаём этот initial в формы
#
#

class FormCollection:

    def __iter__(self):
        return iter(self.forms)

    def __init__(self, form_class=None, prefix=None,
                 data=None, files=None,
                 initial=None, parent_instance=None, parent_field=None,
                 min_values=None, max_values=None):
        assert form_class, '"form_class" parameter must be set'
        assert prefix, '"prefix" parameter must be set'

        self.prefix = prefix
        self.forms = []

        if data:
            data_list = []
            pattern = re.compile(f'{self.prefix}-(\d+)-(.+)')

            for param_name, value in data.items():
                if param_name.startswith(self.prefix):
                    match = re.search(pattern, param_name)
                    if match:
                        data_list.append(
                            (match.group(1), match.group(2), value)
                        )

            data_list.sort(key=lambda x: x[0])
            groups = groupby(data_list, lambda x: x[0])

            counter = 0
            for ind, values in groups:
                fields = {}
                for value in values:
                    fields.update({value[1]: value[2]})
                self.forms.append(
                    form_class(data=fields)
                )
                counter += 1

            print(self.forms)

    def is_valid(self):
        is_valid_all = True

        for form in self.forms:
            if not form.is_valid():
                is_valid_all = False

        return is_valid_all

    def save(self):
        for form in self.forms:
            form.instance.recipe = self.parent_instance
            form.save()

