from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('search/', views.ingredient_search, name='ingredient_search'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path("recipes/", views.recipe_list, name="recipe_list"),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),

    path("dashboard/recipes/", views.admin_recipes, name="admin_recipes"),
    path('recipe/edit/<int:pk>/', views.edit_recipe, name='edit_recipe'),
    path('recipe/delete/<int:pk>/', views.delete_recipe, name='delete_recipe'),
    path("profile/", views.profile, name="profile"),

    path("recipe/<int:recipe_id>/toggle-favorite/",
         views.toggle_favorite,
         name="toggle_favorite"),
    path('favorites/', views.favorites, name='favorites'),
    path('recipe/<int:pk>/review/', views.add_review, name='add_review'),
    path('review/<int:pk>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:pk>/delete/', views.delete_review, name='delete_review'),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("dashboard/users/", views.user_list, name="user_list"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/preferences/", views.edit_preferences, name="edit_preferences"),

    path(
    'dashboard/recipes/feature/<int:id>/',
    views.toggle_featured_recipe,
    name='toggle_featured_recipe'
),
    path("ai-recipes/", views.ai_recipe_suggester, name="ai_recipes"),

    path("ai-chat/", views.ai_chat_page, name="ai_chat"),
    path("ai-chat/api/", views.ai_chat_api, name="ai_chat_api"),
    path("ai/improve-steps/", views.improve_steps_ai, name="improve_steps_ai"),
    path("ai/dietary/", views.dietary_converter, name="dietary_converter"),
    path("ai/convert-recipe/<int:pk>/", views.convert_recipe_ai, name="convert_recipe_ai"),
    path(
    "ai/nutrition/<int:recipe_id>/",
    views.nutrition_recipe,
    name="nutrition_recipe"
),





]
