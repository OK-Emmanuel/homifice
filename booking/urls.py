from django.urls import path
from booking import views

# Define the application namespace
app_name = "booking"

# URL patterns for the booking app
urlpatterns = [
    # URL pattern for checking room availability
    path("check_room_availability/", views.check_room_availability, name="check_room_availability"),
    
    # URL pattern for adding a room to selection
    path("add_to_selection/", views.add_to_selection, name="add_to_selection"),
   
    # URL pattern for deleting a room from selection
    path("delete_selection/", views.delete_selection, name="delete_selection")
]
