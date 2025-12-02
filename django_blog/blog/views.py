# blog/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm  # import accordingly

def home(request):
    return render(request, "blog/home.html")


def register(request):
    """
    User registration view. Uses CustomUserCreationForm to create a user.
    After successful registration, user is redirected to login page.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})


@login_required
def profile(request):
    """
    Profile view to view & edit user's profile and basic info.
    Uses UserUpdateForm and ProfileUpdateForm (if Profile model is present).
    """
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if hasattr(request.user, "profile"):
            profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        else:
            profile_form = None

        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                profile_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile) if hasattr(request.user, "profile") else None

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "blog/profile.html", context)
