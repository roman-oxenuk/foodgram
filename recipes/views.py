import csv
import io

from django.http import FileResponse
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.template.response import TemplateResponse
from django_weasyprint import WeasyTemplateResponseMixin, WeasyTemplateResponse

from .models import Recipe, Tag, Ingredient, IncludedInRecipe
from .forms import TagsFilterForm, RecipeCreateForm, FormCollection, IncludedInRecipeForm


def suggest_ingredient_view(request):
    query = request.GET.get('query')
    if query:
        ingredients_qs = Ingredient.objects.select_related(
            'units'
        ).filter(
            name__startswith=query
        ).all()
        suggesstions = [
            {
                'id': ing.pk,
                'title': ing.name,
                'dimension': ing.units.short_name
            }
            for ing in ingredients_qs
        ]
        return JsonResponse(suggesstions, safe=False)
    return JsonResponse([], safe=False)


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


class RecipeCreateView(CreateView):

    model = Recipe
    template_name = 'recipes/create.html' # fields = ('title', 'image', 'description', 'tags', 'time_to_cook')
    form_class = RecipeCreateForm

    form_collection_class = FormCollection
    form_collection_prefix = 'ingredients-collection'
    ingredient_form = IncludedInRecipeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'instance': Recipe.objects.first()
        })
        return kwargs

    def get_form_collection_kwargs(self):
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.form_collection_prefix,
            'form_class': self.ingredient_form,
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_form_collection(self, form_class=None):
        return self.form_collection_class(**self.get_form_collection_kwargs())

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()

        if 'form_collection' not in kwargs:
            kwargs['form_collection'] = self.get_form_collection()

        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None

        form = self.get_form()
        form_collection = self.get_form_collection()

        if form.is_valid() and form_collection.is_valid():
            self.object = form.save()
            form_collection.parent_instance = self.object
            form_collection.save()
            return HttpResponseRedirect('/recipes/create/')
        else:
            return self.render_to_response(self.get_context_data(form=form, form_collection=form_collection))


def download_ingredients_csv(request):
    all_ingredients = Ingredient.objects.select_related('units').all()
    all_ingredients = [(ing.name, ing.units.short_name) for ing in all_ingredients]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ingredients.csv"'

    writer = csv.writer(response)
    writer.writerows(all_ingredients)

    return response


class IngredientsDownloadView(WeasyTemplateResponseMixin, ListView):
# class IngredientsDownloadView(ListView):
    model = Ingredient
    template_name = 'recipes/ingredients_file.html'

    pdf_filename = 'ingredients.pdf'
    pdf_attachment = False


def download_pdf_func(request):
    all_ingredients = Ingredient.objects.select_related('units').all()

    return WeasyTemplateResponse(
        filename='ingredients.pdf',
        attachment=False,
        content_type='application/pdf',

        request=request,
        template='recipes/ingredients_file.html',
        context={'object_list': all_ingredients}
    )

    # return TemplateResponse(
    #     request=request,
    #     template='recipes/ingredients_file.html',
    #     context={'object_list': all_ingredients}
    # )
