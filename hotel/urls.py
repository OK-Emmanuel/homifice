from django.urls import path
from hotel import views

# Define the application namespace
app_name = "hotel"

# URL patterns for the hotel app
urlpatterns = [
    # URL pattern for the index view
    path("", views.index, name="index"),
    
    # URL pattern for the hotel detail view
    path("detail/<slug>/", views.hotel_detail, name="hotel_detail"),
    
    # URL pattern for the room type detail view
    path("detail/<slug:slug>/room-type/<slug:rt_slug>/", views.room_type_detail, name="room_type_detail"),
    
    # URL pattern for the selected rooms view
    path("selected_rooms/", views.selected_rooms, name="selected_rooms"),

    # URL pattern for checkout
    path("checkout/<booking_id>/ ", views.checkout, name="checkout"),
    
    # URL pattern for room update
    path("update_room_status/", views.update_room_status, name="update_room_status"),

    # URL pattern for the payment success
    path("success/<booking_id>/", views.payment_success, name="payment_success"),
    
    # URL pattern for the payment failure
    path("failed/<booking_id>/", views.payment_failed, name="payment_failed"),
]
