from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from .models import Recipe, Tag
from .forms import TagsFilterForm


class RecipeIndexListView(ListView):

    model = Recipe
    template_name = 'index.html'

    def get_queryset(self):
        qs = super().get_queryset()

        if 'filters' in self.request.GET:
            filters = self.request.GET.getlist('filters')
            qs = qs.filter(tags__name__in=filters).distinct()

        return qs

    def get_all_tags(self):
        return Tag.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'all_tags': self.get_all_tags()})
        return context


class RecipeDetailView(DetailView):

    model = Recipe
    template_name = 'recipes/detail.html'
