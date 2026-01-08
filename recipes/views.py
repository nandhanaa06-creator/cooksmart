
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Recipe 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from .models import Favorite , Review
from django.db.models import Avg, Exists, OuterRef







from django.db.models import Avg, Exists, OuterRef, Value, BooleanField

def home(request):
    foods = Recipe.objects.filter(is_featured=True).annotate(
        avg_rating=Avg('reviews__rating')
    )

    if request.user.is_authenticated:
        foods = foods.annotate(
            is_favorited=Exists(
                Favorite.objects.filter(
                    user=request.user,
                    recipe=OuterRef('pk')
                )
            )
        )
    else:
        foods = foods.annotate(
            is_favorited=Value(False, output_field=BooleanField())
        )

    return render(request, 'recipes/home.html', {
        "foods": foods
    })


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'recipes/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'recipes/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, 'recipes/signup.html')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'recipes/signup.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return render(request, 'recipes/login.html')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'recipes/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def ingredient_search(request):
    recipes = []
    query = request.GET.get('ingredients')

    if query:
        user_ingredients = [
            i.strip().lower() for i in query.split(',')
        ]

        for recipe in Recipe.objects.all():
            recipe_ingredients = recipe.ingredients.lower()

            if any(ing in recipe_ingredients for ing in user_ingredients):
                recipes.append(recipe)

    return render(
        request,
        'recipes/ingredient_search.html',
        {'recipes': recipes}
    )


def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    context = {
        "total_users": User.objects.count(),
        "total_recipes": Recipe.objects.count(),
    }
    return render(request, "recipes/admin_dashboard.html", context)

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

def is_admin(user):
    return user.is_staff






@login_required
def add_recipe(request):
    if request.method == "POST":

        instructions_list = request.POST.getlist("instructions[]")
        instructions_text = "\n".join(instructions_list)

        Recipe.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            category=request.POST.get("category"),
            cook_time=request.POST.get("cook_time"),
            servings=request.POST.get("servings"),
            difficulty=request.POST.get("difficulty"),
            ingredients=request.POST.get("ingredients"),
            instructions=instructions_text,
            image=request.FILES.get("image"),
            video=request.FILES.get("video"),
            user=request.user
        )

        return redirect("home")   # ✅ POST must return

    # ✅ VERY IMPORTANT (for GET request)
    return render(request, "recipes/add_recipe.html")







def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    avg_rating = recipe.reviews.aggregate(
        Avg('rating')
    )['rating__avg']

    user_rating = None
    is_favorite = False

    if request.user.is_authenticated:
        review = Review.objects.filter(
            user=request.user,
            recipe=recipe
        ).first()

        if review:
            user_rating = review.rating

        is_favorite = Favorite.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists()

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'avg_rating': avg_rating,
        'user_rating': user_rating,
        'is_favorite': is_favorite,
    })


@staff_member_required
def admin_recipes(request):
    recipes = Recipe.objects.all().order_by("-created_at")
    return render(request, "recipes/admin_recipes.html", {
        "recipes": recipes
    })

@staff_member_required
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)
    recipe.delete()
    return redirect('admin_recipes')


def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)

    if request.method == 'POST':
        recipe.title = request.POST['title']
        recipe.ingredients = request.POST['ingredients']
        recipe.instructions = request.POST['instructions']

        if 'image' in request.FILES:
            recipe.image = request.FILES['image']

        if 'video' in request.FILES:
            recipe.video = request.FILES['video']

        recipe.save()
        return redirect('admin_recipes')

    return render(request, 'recipes/edit_recipe.html', {'recipe': recipe})

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    recipe_count = Recipe.objects.filter(user=request.user).count()

    return render(request, "recipes/profile.html", {
        "profile": profile,   # 🔴 THIS WAS THE PROBLEM
        "recipe_count": recipe_count
    })

from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Avg, Exists, OuterRef, Value, BooleanField
from .models import Recipe, Favorite


def recipe_list(request):
    recipes = Recipe.objects.annotate(
        avg_rating=Avg("reviews__rating")
    )

    # 🔹 QUICK RECIPE FILTER
    recipe_type = request.GET.get("type")

    if recipe_type == "quick":
        recipes = recipes.filter(cook_time__lte=15)

    # 🔹 FAVORITE STATUS
    if request.user.is_authenticated:
        recipes = recipes.annotate(
            is_favorited=Exists(
                Favorite.objects.filter(
                    user=request.user,
                    recipe=OuterRef("pk")
                )
            )
        )
    else:
        recipes = recipes.annotate(
            is_favorited=Value(False, output_field=BooleanField())
        )

    return render(request, "recipes/all_recipes.html", {
        "recipes": recipes,
        "recipe_type": recipe_type,
    })


@login_required
def toggle_favorite(request, recipe_id):
    if request.method == "POST":
        recipe = get_object_or_404(Recipe, id=recipe_id)

        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )

        if not created:
            favorite.delete()
            return JsonResponse({"status": "removed"})
        else:
            return JsonResponse({"status": "added"})

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('recipe')
    return render(request, 'recipes/favorites.html', {'favorites': favorites})





@login_required
def add_review(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("review")

        Review.objects.update_or_create(
            recipe=recipe,
            user=request.user,
            defaults={
                'rating': rating,
                'comment': comment
            }
        )

    return redirect('recipe_detail', recipe_id=pk)


@login_required
def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)

    if request.method == "POST":
        review.rating = request.POST.get("rating")
        review.comment = request.POST.get("review")
        review.save()
        return redirect('recipe_detail', recipe_id=review.recipe.id)

    return render(request, 'recipes/edit_review.html', {
        'review': review
    })


@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    recipe_id = review.recipe.id
    review.delete()
    return redirect('recipe_detail', recipe_id=recipe_id)


def is_admin(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all().order_by("-date_joined")
    return render(request, "recipes/user_list.html", {
        "users": users
    })
@login_required
@user_passes_test(is_admin)
def dashboard(request):
    return render(request, "recipes/dashboard.html", {
        "total_users": User.objects.count(),
        "total_recipes": Recipe.objects.count(),
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile, Recipe

from .models import Profile, Recipe, Favorite

@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    recipe_count = Recipe.objects.filter(user=request.user).count()
    favorite_count = request.user.favorites.count()  # ✅ cleaner

    return render(request, "recipes/profile.html", {
        "profile": profile,
        "recipe_count": recipe_count,
        "favorite_count": favorite_count,
    })




@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        request.user.username = request.POST.get("username", request.user.username)
        request.user.email = request.POST.get("email", request.user.email)

        profile.loves_spicy = "loves_spicy" in request.POST
        profile.avoid_onion = "avoid_onion" in request.POST
        profile.low_salt = "low_salt" in request.POST

        if request.FILES.get("profile_image"):
            profile.profile_image = request.FILES["profile_image"]

        request.user.save()
        profile.save()

        return redirect("profile")

    return render(request, "recipes/edit_profile.html", {"profile": profile})

@login_required
def edit_preferences(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.loves_spicy = "loves_spicy" in request.POST
        profile.avoid_onion = "avoid_onion" in request.POST
        profile.low_salt = "low_salt" in request.POST
        profile.save()

        return redirect("profile")

    return render(request, "recipes/edit_preferences.html", {
        "profile": profile
    })



from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from .models import Recipe


@staff_member_required
def toggle_featured_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    recipe.is_featured = not recipe.is_featured
    recipe.save()
    return redirect('admin_recipes')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .ai import ask_ai


@login_required
def ai_recipe_suggester(request):
    answer = None

    if request.method == "POST":
        ingredients = request.POST.get("ingredients")

        # ✅ CORE AI PROMPT (CONSISTENT + PRACTICAL)
        prompt = f"""
Generate a cooking recipe using the following ingredients:

{ingredients}

Rules:
- Assume basic kitchen items are available
- Provide ingredients list with quantities
- Provide step-by-step cooking instructions
- Include cooking time
- Include 2 helpful cooking tips
- Keep it simple and practical
"""

        answer = ask_ai(prompt)

    return render(
        request,
        "recipes/ai_recipes.html",
        {"answer": answer}
    )


from django.shortcuts import render
from django.http import JsonResponse
from .ai import ask_ai

def ai_chat_page(request):
    return render(request, "recipes/ai_chat.html")


def ai_chat_api(request):
    if request.method == "POST":
        message = request.POST.get("message", "").strip()

        if not message:
            return JsonResponse({"reply": "Please enter a message."})

        try:
            reply = ask_ai(message)
        except Exception as e:
            reply = "AI server is not responding. Please try again later."

        return JsonResponse({"reply": reply})

    return JsonResponse({"reply": "Invalid request"}, status=400)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .ai import improve_steps
import json

@login_required
def improve_steps_ai(request):
    if request.method == "POST":
        data = json.loads(request.body)
        steps = data.get("steps", "")

        improved = improve_steps(steps)

        return JsonResponse({"steps": improved})

    return JsonResponse({"error": "Invalid request"}, status=400)

from .ai import convert_recipe_diet

@login_required
def dietary_converter(request):
    output = None

    if request.method == "POST":
        recipe = request.POST.get("recipe")
        diet_type = request.POST.get("diet_type")

        output = convert_recipe_diet(recipe, diet_type)

    return render(
        request,
        "recipes/dietary_converter.html",
        {"output": output}
    )
from django.views.decorators.http import require_POST


@require_POST
@login_required
def convert_recipe_ai(request, pk):
    try:
        recipe = get_object_or_404(Recipe, id=pk)

        data = json.loads(request.body.decode("utf-8"))
        diet = data.get("diet_type")

        if not diet:
            return JsonResponse(
                {"error": "Diet type is missing"},
                status=400
            )

        recipe_text = f"""
Ingredients:
{recipe.ingredients}

Instructions:
{recipe.instructions}
"""

        result = convert_recipe_diet(recipe_text, diet)

        return JsonResponse({"result": result})

    except Exception as e:
        # 🔥 THIS IS THE KEY PART
        return JsonResponse(
            {"error": str(e)},
            status=500
        )



from django.views.decorators.http import require_POST
from .ai import nutrition_aware_recipe

@login_required
@require_POST

def nutrition_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    recipe_text = f"""
{recipe.ingredients}
{recipe.instructions}
"""

    result = nutrition_aware_recipe(recipe_text)
    return JsonResponse({"result": result})
