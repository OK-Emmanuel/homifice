from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from userauths.models import User, Profile
from userauths.forms import UserRegisterForm


def RegisterView(request, *args, **kwargs):
    if request.user.is_authenticated:
        messages.warning(request, f"You are already logged in")
        return redirect("hotel:index")

    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)  # Get the unsaved user instance
        user.save()  # Save the user instance

        full_name = form.cleaned_data.get("full_name")
        phone = form.cleaned_data.get("phone")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")

        # Authenticate and login user
        user = authenticate(email=email, password=password)
        login(request, user)

        # Save profile information
        profile = Profile.objects.get(user=user)  # Fetch profile associated with the new user
        profile.full_name = full_name
        profile.phone = phone
        profile.save()

        messages.success(request, f"Ease! {full_name}, your account was created successfully")
        return redirect("hotel:index")

    context = {"form": form}
    return render(request, "userauths/sign-up.html", context)


    

def loginViewTemp(request):

    # Retrun logged in user to homepage when requesting to sign in
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("hotel:index")
    

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_query = User.objects.get(email=email)
            user_auth = authenticate(request, email=email, password=password)

            # return user to their tracked url
            if user_query is not None:
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


def LogoutView(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect("userauths:sign-in")