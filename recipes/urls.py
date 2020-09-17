from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.RecipeIndexListView.as_view()),
    path('ingredients/', views.suggest_ingredient_view, name='suggest_ingredient'),
    path('recipes/create/', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('recipes/<slug>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('download_csv/', views.download_ingredients_csv, name='recipe_download_csv'),
    # path('download_pdf/', views.download_ingredients_pdf, name='recipe_download_pdf'),
    # path('download_pdf/', views.DownloadIngredientsView.as_view(), name='recipe_download_pdf'),
    path('download_pdf/', views.IngredientsDownloadView.as_view(), name='recipe_download_pdf'),
    path('download_pdf_func/', views.download_pdf_func, name='recipe_download_pdf_func'),
]
