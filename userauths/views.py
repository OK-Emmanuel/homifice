from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from userauths.models import User, Profile
from userauths.forms import UserRegisterForm

# View for user registration
def RegisterView(request, *args, **kwargs):
    if request.user.is_authenticated:
        # Redirect authenticated users to the home page with a warning message
        messages.warning(request, "You are already logged in")
        return redirect("hotel:index")

    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        # Save the new user instance
        user = form.save(commit=False)
        user.save()

        # Get cleaned data from the form
        full_name = form.cleaned_data.get("full_name")
        phone = form.cleaned_data.get("phone")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")

        # Authenticate and log in the new user
        user = authenticate(email=email, password=password)
        login(request, user)

        # Save profile information
        profile = Profile.objects.get(user=user)
        profile.full_name = full_name
        profile.phone = phone
        profile.save()

        # Display success message and redirect to the home page
        messages.success(request, f"Welcome! {full_name}, your account was created successfully")
        return redirect("hotel:index")

    context = {"form": form}
    return render(request, "userauths/sign-up.html", context)

# View for user login
def loginViewTemp(request):
    if request.user.is_authenticated:
        # Redirect authenticated users to the home page with a warning message
        messages.warning(request, "You are already logged in")
        return redirect("hotel:index")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_query = User.objects.get(email=email)
            user_auth = authenticate(request, email=email, password=password)

            if user_query is not None:
                # Log in the user and redirect to the tracked URL or home page
                login(request, user_auth)
                messages.success(request, "You are logged in")
                next_url = request.GET.get("next", "hotel:index")
                return redirect(next_url)
            else:
                messages.error(request, "Username or password does not exist")
                return redirect("userauths:sign-in")
        except:
            messages.error(request, "User does not exist")
            return redirect("userauths:sign-in")

    return render(request, "userauths/sign-in.html")

# View for user logout
def LogoutView(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect("userauths:sign-in")
