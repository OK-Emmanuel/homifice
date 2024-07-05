from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from hotel.models import Hotel, Booking
from userauths.models import Profile 
from userauths.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
# Create your views here.
@login_required

def dashboard(request):
    bookings = Booking.objects.filter(user=request.user, payment_status="paid") 
    total_spent = Booking.objects.filter(user=request.user, payment_status='paid').aggregate(amount=models.Sum("total"))
    total_spent_formatted = "{:.2f}".format(total_spent['amount'])  # Format to 2 decimal places

    # print(total_spent_formatted)
    context ={
        "bookings": bookings,
        "total_spent": total_spent,
        "total_spent_to_display": total_spent_formatted,  


    }
    
    return render(request, 'user_dashboard/dashboard.html', context)


@login_required
def booking_detail(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id, user=request.user, payment_status="paid")
    context = {
        "booking": booking
    }
    return render(request, "user_dashboard/booking_detail.html", context)


@login_required
def bookings(request):
    booking = Booking.objects.filter(user=request.user, payment_status="paid")
    context = {
        "booking": booking
    }
    return render(request, "user_dashboard/booking.html", context)


@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        userForm = UserUpdateForm(request.POST, instance=request.user)
        profileForm = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("user_dashboard:profile")
    else:
        userForm = UserUpdateForm(instance=request.user)
        profileForm = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "profile": profile,
        "userForm": userForm,
        "profileForm": profileForm,
    }
    return render(request, "user_dashboard/profile.html", context)

