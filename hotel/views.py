import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from hotel.models import Hotel, Booking, ActivityLog, StaffOnDuty, Room, RoomType, Coupon, HotelFaqs, HotelFeatures, HotelGallery

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

        if request.method == "POST":
            for h_id, item in request.session['selection_data_obj'].items():
                # Execute code on submission
                id = int(item['hotel_id'])
                checkin = item['checkin']
                checkout = item['checkout']
                adult = int(item['adult'])  
                children = int(item['children'])
                room_type_ = int(item['room_type'])
                room_id = int(item['room_id'])
                room_type = RoomType.objects.get(id=room_type_)

                user = request.user
                hotel = Hotel.objects.get(id=id)
                room = Room.objects.get(id=room_id)
                room_type = RoomType.objects.get(id=room_type_)
            
            # Debugging: Log the session data
            print(f"Check-in date from session: {checkin}")
            print(f"Check-out date from session: {checkout}")

            # Calculate total booked days
            date_format = "%Y-%m-%d"
            checkin_date = datetime.datetime.strptime(checkin, date_format)
            checkout_date = datetime.datetime.strptime(checkout, date_format)
            time_difference = checkout_date - checkin_date
            total_days = time_difference.days

            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')

            booking = Booking.objects.create(
                hotel=hotel,
                room_type=room_type,
                check_in_date=checkin,
                check_out_date=checkout,
                total_days=total_days,
                num_adults=adult,
                num_children=children,
                full_name=full_name,
                email=email,
                phone=phone,
                user=request.user or None
            )
 
            for h_id, item in request.session['selection_data_obj'].items():
                room_id = int(item["room_id"])
                room = Room.objects.get(id=room_id)
                booking.room.add(room)

                room_count += 1
                days = total_days
                price = room_type.price
                room_price = price * room_count
                total = room_price * days
            
            booking.total += float(total)
            booking.before_discount += float(total)
            booking.save()

            return redirect("hotel:checkout", booking.booking_id)


        hotel = None
        for h_id, item in request.session['selection_data_obj'].items():
            id = int(item['hotel_id'])
            checkin = item['checkin']
            checkout = item['checkout']
            adult = int(item['adult'])  
            children = int(item['children'])
            room_type_ = int(item['room_type'])
            room_id = int(item['room_id'])
            room_type = RoomType.objects.get(id=room_type_)
            
            # Debugging: Log the session data
            print(f"Check-in date from session: {checkin}")
            print(f"Check-out date from session: {checkout}")

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
        messages.warning(request, "No selected room yet")
        return redirect("/")


def checkout(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)
    if request.method == "POST":
            code = request.POST.get('code')
            try:
                coupon = Coupon.objects.get(code__iexact=code, active=True)
                if coupon in booking.coupons.all():
                    messages.warning(request, "Coupon already applied to this booking.")
                    return redirect("hotel:checkout", booking.booking_id)
                
                else:
                    if coupon.type == "Percentage":
                        discount = booking.total * (coupon.discount / 100)
                    else:
                        discount = coupon.discount

                    booking.coupons.add(coupon)
                    booking.total -= discount
                    booking.saved += discount
                    booking.save()


                    messages.success(request, "Coupon applied successfully.")
                    return redirect("hotel:checkout", booking.booking_id)
                

                # print("coupon ============", coupon)
            except:
                messages.warning(request, "Invalid Coupon Code")
                # print("coupon does note exist")
    context = {
        "booking": booking
    }

    return render(request,"hotel/checkout.html", context)

