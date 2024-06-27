from django.urls import path
from userauths import views

# Define the application namespace
app_name = "userauths"

# URL patterns for the userauths app
urlpatterns = [
    # URL pattern for user registration
    path("sign-up/", views.RegisterView, name="sign-up"),
    
    # URL pattern for user login
    path("sign-in/", views.loginViewTemp, name="sign-in"),
    
    # URL pattern for user logout
    path("sign-out/", views.LogoutView, name="sign-out"),
]
