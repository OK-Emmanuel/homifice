from django.shortcuts import render

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