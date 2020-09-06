from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from .models import Recipe, Tag
from .forms import TagsFilterForm


class RecipeIndexListView(FormMixin, ListView):

    model = Recipe
    template_name = 'index.html'
    form_class = TagsFilterForm

    def get_form_kwargs(self):
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }
        if self.request.method in ('GET'):
            kwargs.update({
                'data': self.request.GET,
            })
        return kwargs

    def get_queryset(self):
        qs = super().get_queryset()
        form = self.form_class(**self.get_form_kwargs())
        if form.is_valid():
            tags_ids = [tag.id for tag in form.cleaned_data['tags']]
            qs = qs.filter(tags__pk__in=tags_ids)
        return qs


class RecipeDetailView(DetailView):

    model = Recipe
    template_name = 'recipes/detail.html'
