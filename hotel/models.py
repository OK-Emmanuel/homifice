from django.db import models
from django.utils.text import slugify
from django.utils.html import mark_safe
import shortuuid
from userauths.models import User
from shortuuid.django_fields import ShortUUIDField
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager

# Choices for hotel status
HOTEL_STATUS = (
    ("Draft", "Draft"),
    ("Disabled", "Disabled"),
    ("Rejected", "Rejected"),
    ("In Review", "In Review"),
    ("Live", "Live"),
)

# Icon Types
ICON_TYPE = (
    ("Bootstrap Icons", "Bootstrap Icons"),
    ("FontAwesome", "Fontawesome Icons"),
    ("Boxicon", "Boxicons"),
    ("Remixicon", "Remixicon"),
)

# Payment Status for Hotel Rooms
PAYMENT_STATUS = (
    ("paid", "paid"),
    ("pending", "pending"),
    ("processing", "processing"),
    ("cancelled", "cancelled"),
    ("initiated", "initiated"),
    ("failed", "failed"),
    ("refunding", "refunding"),
    ("refunded", "refunded"),
    ("expired", "expired"),
)

# Hotel model definition
class Hotel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # The hotel lister
    name = models.CharField(max_length=255)
    description = CKEditor5Field(null=True, blank=True, config_name='extends')
    image = models.FileField(upload_to="hotel_gallery")
    address = models.CharField(max_length=500)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    status = models.CharField(max_length=20, choices=HOTEL_STATUS, default="Live")
    
    tags = TaggableManager(blank=True)
    views = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    hotelID = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz")
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    
    # Social media links
    website = models.CharField(max_length=2048, null=True, blank=True)
    facebook = models.CharField(max_length=2048, null=True, blank=True)
    twitter = models.CharField(max_length=2048, null=True, blank=True)
    instagram = models.CharField(max_length=2048, null=True, blank=True)
    youtube = models.CharField(max_length=2048, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Automatically generate a slug if it doesn't exist
        if not self.slug:
            uuid_key = shortuuid.uuid()
            uniqueID = uuid_key[:4]
            self.slug = slugify(self.name) + '-' + str(uniqueID.lower())
        super(Hotel, self).save(*args, **kwargs)
    
    # Custom HTML/CSS for image thumbnail
    def thumbnail(self):
        if self.image:
            return mark_safe("<img src='%s' width='50' height='50' style='object-fit: cover; border-radius 7px;' />" % (self.image.url))
        return "No Image"
    
    thumbnail.short_description = 'Thumbnail'
    
    # Methods to get related objects
    def hotel_gallery(self):
        return HotelGallery.objects.filter(hotel=self)
    
    def hotel_room_types(self):
        return RoomType.objects.filter(hotel=self)

# Hotel gallery model
class HotelGallery(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    image = models.FileField(upload_to="hotel_gallery")
    hotelGalleryID = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz")
    
    def __str__(self):
        return str(self.hotel.name)
    
    class Meta:
        verbose_name_plural = "Hotel Gallery"

# Hotel features model
class HotelFeatures(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    icon_type = models.CharField(max_length=100, null=True, choices=ICON_TYPE)
    icon = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = "Hotel Features"

# Hotel FAQs model
class HotelFaqs(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.question)
    
    class Meta:
        verbose_name_plural = "Hotel FAQs"

# Room type model
class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    number_of_beds = models.PositiveBigIntegerField(default=0)
    room_capacity = models.PositiveIntegerField(default=0)
    roomTypeID = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz")
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.type} - {self.hotel.name} - {self.price}"
    
    class Meta:
        verbose_name_plural = "Room Type"
    
    def rooms_count(self):
        return Room.objects.filter(room_type=self).count()
    
    def save(self, *args, **kwargs):
        # Automatically generate a slug if it doesn't exist
        if not self.slug:
            uuid_key = shortuuid.uuid()
            uniqueID = uuid_key[:4]
            self.slug = slugify(self.type) + '-' + str(uniqueID.lower())
        super(RoomType, self).save(*args, **kwargs)

# Room model
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=1000)
    is_available = models.BooleanField(default=True)
    RoomID = ShortUUIDField(unique=True, length=10, alphabet="abcdefghijklmnopqrstuvwxyz")
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.room_type.type} - {self.hotel.name}"
    
    class Meta:
        verbose_name_plural = "Rooms"
    
    def price(self):
        return self.room_type.price
    
    def number_of_beds(self):
        return self.room_type.number_of_beds

# Booking model
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    
    # Connect booking and room
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ManyToManyField(Room)
    before_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    saved = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    check_in_date = models.DateField()
    check_out_date = models.DateField(null=True, blank=True)
    
    total_days = models.PositiveIntegerField(default=0)
    num_adults = models.PositiveIntegerField(default=1)
    num_children = models.PositiveIntegerField(default=0)
    
    checked_in = models.BooleanField(default=False)
    checked_out = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=False)
    
    checked_in_tracker = models.BooleanField(default=False)
    checked_out_tracker = models.BooleanField(default=False)
    coupons = models.ManyToManyField("hotel.Coupon", blank=True)
    
    date = models.DateTimeField(auto_now_add=True)
    stripe_payment_intent = models.CharField(max_length=1000, null=True, blank=True)
    successID = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz", null=True, blank=True)
    booking_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz")
    
    def __str__(self):
        return f"{self.booking_id}"
    
    # Count rooms
    def rooms(self):
        return self.room.all().count()

# Activity log model
class ActivityLog(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    guest_out = models.DateField()
    guest_in = models.DateField()
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.booking}"

# Staff on duty model
class StaffOnDuty(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.staff_id}"

# Coupon model
class Coupon(models.Model):
    code = models.CharField(max_length=100)
    type = models.CharField(max_length=100, default="Percentage")
    discount = models.DecimalField(decimal_places=2, max_digits=100, default=1.00)
    redemptions = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateTimeField()
    couponId = ShortUUIDField(unique=True, length=10, max_length=50)

    def __str__(self):
        return f"{self.code}" 