from django.shortcuts import render, redirect
from django.contrib import messages
from  hotel.models import Hotel, Booking, ActivityLog, StaffOnDuty, Room, RoomType, HotelFaqs, HotelFeatures, HotelGallery


# Create your views here.
def index(request):
    hotels = Hotel.objects.filter(status="Live")
    context = {
        "hotels": hotels
    }
    return render(request, "hotel/hotel.html", context)

def hotel_detail(request, slug):
    #  Retrieve a single object - live hotel
    hotel = Hotel.objects.get(status="Live", slug=slug)
    context = {
          "hotel":hotel,
    }
    return render(request, "hotel/hotel_detail.html", context)

# Describe the kinds of rooms in each hotel
def room_type_detail(request, slug, rt_slug):
    hotel = Hotel.objects.get(status="Live", slug=slug)
    room_type = RoomType.objects.get(hotel=hotel, slug=rt_slug)
    rooms = Room.objects.filter(room_type=room_type, is_available=True)

    # get queries from url
    id = request.GET.get("hotel-id")
    checkin = request.GET.get("checkin")
    checkout = request.GET.get("checkout")
    adult = request.GET.get("adult")
    children = request.GET.get("children")

    context = {
        "hotel": hotel,
        "room_type": room_type,
        "rooms": rooms,
        "checkin": checkin,
        "checkout": checkout,
        "adult": adult,
        "children": children,
    }

    return render(request, "hotel/room_type_detail.html", context)

def selected_rooms(request):
    total = 0
    room_count = 0
    total_days = 0
    adult = 0
    children = 0
    checkin = ""
    checkout = ""

    if 'selection_data_obj' in request.session:
        for h_id, item in request.session['selection_data_obj'].items():
            print(h_id, item)
    else:
        messages.warning(request, "No selected room yet")
        return redirect("/")
    
    return render(request, "hotel/selected_rooms.html")