from django.contrib import admin
from hotel.models import Hotel, Booking, ActivityLog, StaffOnDuty, Room, RoomType, HotelFaqs, HotelFeatures, HotelGallery, Coupon

# Inline model for HotelGallery to be displayed within the Hotel admin page
class HotelGalleryInline(admin.TabularInline):
    model = HotelGallery

# Custom admin class for Hotel model
class HotelAdmin(admin.ModelAdmin):
    # Include HotelGalleryInline in the admin interface
    inlines = [HotelGalleryInline]
    # Fields to display in the list view
    list_display = ['thumbnail', 'name', 'user', 'status']
    # Automatically generate slug from the name
    prepopulated_fields = {"slug": ("name", )}

# Registering the models with their respective admin classes
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Booking)
# admin.site.register(ActivityLog)
# admin.site.register(StaffOnDuty)
admin.site.register(Room)
admin.site.register(Coupon)
admin.site.register(RoomType)
admin.site.register(HotelFaqs)
admin.site.register(HotelFeatures)
admin.site.register(HotelGallery)
