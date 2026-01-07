from django.apps import AppConfig


class RecipesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    name = 'recipes'

from django.apps import AppConfig

def ready(self):
        import recipes.signals
