from django.urls import path
from user_dashboard import views

app_name = 'user_dashboard'


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path("booking_detail/<booking_id>", views.booking_detail, name="booking_detail"),
    path("bookings/", views.bookings, name="bookings"),
    path("profile/", views.profile, name="profile"),
]