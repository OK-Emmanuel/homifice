import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from hotel.models import Hotel, Booking, ActivityLog, StaffOnDuty, Room, RoomType, HotelFaqs, HotelFeatures, HotelGallery

# Display the list of live hotels on the index page
def index(request):
    hotels = Hotel.objects.filter(status="Live")
    context = {
        "hotels": hotels
    }
    return render(request, "hotel/hotel.html", context)

# Display details of a specific hotel
def hotel_detail(request, slug):
    # Retrieve a single live hotel by slug
    hotel = Hotel.objects.get(status="Live", slug=slug)
    context = {
        "hotel": hotel,
    }
    return render(request, "hotel/hotel_detail.html", context)

# Display details of a specific room type in a hotel
def room_type_detail(request, slug, rt_slug):
    # Retrieve the hotel and room type objects based on slugs
    hotel = Hotel.objects.get(status="Live", slug=slug)
    room_type = RoomType.objects.get(hotel=hotel, slug=rt_slug)
    rooms = Room.objects.filter(room_type=room_type, is_available=True)

    # Get query parameters from the URL
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

# Display the selected rooms and calculate the total cost
def selected_rooms(request):
    total = 0
    room_count = 0
    total_days = 0
    adult = 0
    children = 0
    checkin = ""
    checkout = ""

    if 'selection_data_obj' in request.session:
        hotel = None
        for h_id, item in request.session['selection_data_obj'].items():
            # Retrieve room selection details from session
            id = int(item['hotel_id'])
            checkin = item['checkin']
            checkout = item['checkout']
            adult = int(item['adult'])
            children = int(item['children'])
            room_type_ = int(item['room_type'])
            room_id = int(item['room_id'])
            room_type = RoomType.objects.get(id=room_type_)

            # Calculate total booked days
            date_format = "%Y-%m-%d"
            checkin_date = datetime.datetime.strptime(checkin, date_format)
            checkout_date = datetime.datetime.strptime(checkout, date_format)
            time_difference = checkout_date - checkin_date
            total_days = time_difference.days

            room_count += 1
            days = total_days
            price = room_type.price

            room_price = price * room_count
            total_price = room_price * days

            hotel = Hotel.objects.get(id=id)
        
        context = {
            "data": request.session['selection_data_obj'],
            "total_selected_items": len(request.session['selection_data_obj']),
            "total": total,
            "total_days": total_days,
            "adult": adult,
            "children": children,
            "checkin": checkin,
            "checkout": checkout,
            "hotel": hotel,
        }
        return render(request, "hotel/selected_rooms.html", context)
    else:
        # Display warning message if no room is selected
        messages.warning(request, "No selected room yet")
        return redirect("/")
