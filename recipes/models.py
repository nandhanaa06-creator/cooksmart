from django.db import models
from django.contrib.auth.models import User


from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    category = models.CharField(
        max_length=100,
        blank=True
    )

    cook_time = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Time in minutes"
    )

    # ⭐ IMPORTANT FOR RECIPE SCALING
    servings = models.PositiveIntegerField(
        default=2,
        help_text="Number of servings this recipe makes"
    )

    difficulty = models.CharField(
        max_length=20,
        choices=[
            ("Easy", "Easy"),
            ("Medium", "Medium"),
            ("Hard", "Hard"),
        ],
        default="Medium"
    )

    # Expected format:
    # 1 cup rice
    # 2 eggs
    # 0.5 tsp salt
    ingredients = models.TextField(
        help_text="One ingredient per line (quantity unit ingredient)"
    )

    instructions = models.TextField(
        help_text="One step per line"
    )

    image = models.ImageField(
        upload_to="recipes/images/",
        blank=True,
        null=True
    )

    video = models.FileField(
        upload_to="recipes/videos/",
        blank=True,
        null=True
    )

    is_featured = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.title} ({self.servings} servings)"



class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites"   # ✅ ADD THIS
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorited_by"
    )

    class Meta:
        unique_together = ("user", "recipe")

    def __str__(self):
        return f"{self.user.username} → {self.recipe.title}"



class Review(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.recipe.title} - {self.rating}"

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)

    loves_spicy = models.BooleanField(default=False)
    avoid_onion = models.BooleanField(default=False)
    low_salt = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

