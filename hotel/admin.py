from django.contrib import admin
from  hotel.models import Hotel, Booking, ActivityLog, StaffOnDuty, Room, RoomType, HotelFaqs, HotelFeatures, HotelGallery

# Allow gallery for hotels
class HotelGalleryInline(admin, TabularInline):
    model = HotelGallery
     

class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelGalleryInline]
    list_display = ['thumbnail', 'name', 'user', 'status']
    # Auto slug generation
    prepopulated_fields = {"slug": ("name", )} 

admin.site.register(Hotel, HotelAdmin)
admin.site.register(Booking)
admin.site.register(ActivityLog)
admin.site.register(StaffOnDuty)
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(HotelFaqs)
admin.site.register(HotelFeatures)
admin.site.register(HotelGallery)

