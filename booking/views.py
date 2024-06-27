from django.shortcuts import render, redirect
from django.urls import reverse
from hotel.models import Hotel, Booking, ActivityLog, StaffOnDuty, Room, RoomType, HotelFaqs, HotelFeatures, HotelGallery
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def check_room_availability(request):
    if request.method == "POST":
        # Retrieve data from POST request
        id = request.POST.get("hotel-id")
        checkin = request.POST.get("checkin")
        checkout = request.POST.get("checkout")
        adult = request.POST.get("adult")
        children = request.POST.get("children")
        room_type = request.POST.get("room_type")

        # Get the hotel and room type objects based on the provided data
        hotel = Hotel.objects.get(id=id)
        room_type = RoomType.objects.get(hotel=hotel, slug=room_type)

        # Construct the URL with parameters for room type details
        url = reverse("hotel:room_type_detail", args=[hotel.slug, room_type.slug])
        url_with_params = f"{url}?hotel-id={id}&checkin={checkin}&checkout={checkout}&adult={adult}&children={children}&room_type={room_type}"
        
        # Redirect to the constructed URL
        return HttpResponseRedirect(url_with_params)

def add_to_selection(request):
    # Initialize room selection dictionary
    room_selection = {}
    
    # Populate the room selection dictionary with data from GET request
    room_selection[str(request.GET['id'])] = {
        'hotel_id': request.GET['hotel_id'],
        'hotel_name': request.GET['hotel_name'],
        'room_id': request.GET['room_id'],
        'room_name': request.GET['room_name'],
        'room_price': request.GET['room_price'],
        'room_type': request.GET['room_type'],
        'room_number': request.GET['room_number'],
        'number_of_beds': request.GET['number_of_beds'],
        'checkin': request.GET['checkin'],
        'checkout': request.GET['checkout'],
    }

    # Create or update session for room selection
    if 'selection_data_obj' in request.session:
        if str(request.GET['id']) in request.session['selection_data_obj']:
            # Update the existing selection data with adult and children information
            selection_data = request.session['selection_data_obj']
            selection_data[str(request.GET['id'])]['adult'] = int(room_selection[str(request.GET['id'])]['adult'])
            selection_data[str(request.GET['id'])]['children'] = int(room_selection[str(request.GET['id'])]['children'])
            request.session['selection_data_obj'] = selection_data
        else:
            # Add new room selection to the existing selection data
            selection_data = request.session['selection_data_obj']
            selection_data.update(room_selection)
            request.session['selection_data_obj'] = selection_data
    else:
        # Create new session data object for room selection
        request.session['selection_data_obj'] = room_selection

    # Prepare the response data
    data = {
        "data": request.session['selection_data_obj'],
        "total_selected_items": len(request.session['selection_data_obj'])
    }

    # Return the response as JSON
    return JsonResponse(data)
