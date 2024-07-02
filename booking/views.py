from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.urls import reverse
from hotel.models import Hotel, Booking, ActivityLog, StaffOnDuty, Room, RoomType, HotelFaqs, HotelFeatures, HotelGallery
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime

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
        'room_name': request.GET['room_name'],
        'room_price': request.GET['room_price'],
        'number_of_beds': request.GET['number_of_beds'],
        'room_number': request.GET['room_number'],
        'room_type': request.GET['room_type'],
        'room_id': request.GET['room_id'],
        'checkin': request.GET['checkin'],
        'checkout': request.GET['checkout'],
        'adult': request.GET['adult'],
        'children': request.GET['children']
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


# Delete Selection
def delete_selection(request):
    hotel_id = str(request.GET['id'])
    if 'selection_data_obj' in request.session:
        if hotel_id in request.session['selection_data_obj']:
            selection_data = request.session['selection_data_obj']
            del request.session['selection_data_obj'][hotel_id]
            # Update / refresh selection
            request.session['selection_data_obj'] = selection_data

        total = 0
        total_days = 0
        room_count = 0
        adult = 0
        children = 0
        checkin = ""
        checkout = ""
        hotel = None

        if 'selection_data_obj' in request.session:
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
                total = room_price * days
    
        context = render_to_string(
        "hotel/async/selected_rooms.html", 
            {
                "data": request.session['selection_data_obj'], 
                "total_selected_items": len(request.session['selection_data_obj']),
                "total": total,
                "total_days": total_days,
                "adult":adult,
                "children":children,
                "checkin":checkin,
                "checkout": checkout,
                "hotel":hotel,
            },
        )
    

    return JsonResponse({"data": context, "total_selected_items": len(request.session['selection_data_obj'])}) 