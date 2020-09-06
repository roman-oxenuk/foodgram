from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.RecipeIndexListView.as_view()),
    path('recipes/<slug>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
]
