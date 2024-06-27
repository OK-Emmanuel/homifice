from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from shortuuid.django_fields import ShortUUIDField


# Function to create dynamic image paths for each user
def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (instance.user.id, filename)
    return "user_{0}/{1}".format(instance.user.id, filename)


# Choices for gender and identity types
GENDER = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
)

IDENTITY_TYPE = (
    ("National Identification Number", "National Identification Number"),
    ("Driver's License", "Driver's License"),
    ("International Passport", "International Passport"),
)


# Custom User model inheriting from AbstractUser
class User(AbstractUser):
    full_name = models.CharField(max_length=500, null=True, blank=True)
    username = models.CharField(max_length=500, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)  # For country prefix
    gender = models.CharField(max_length=20, choices=GENDER, default="Other")

    otp = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'  # Use email as the unique identifier for login
    REQUIRED_FIELDS = ['username']  # Required fields for user creation

    def __str__(self):
        return self.username


# Profile model linked to User via OneToOneField
class Profile(models.Model):
    profileID = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvwxyz123")
    image = models.FileField(upload_to=user_directory_path, default="default.jpg", null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=500, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)  # For country prefix
    gender = models.CharField(max_length=20, choices=GENDER, default="Other")
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)

    # Identity verification
    identity_type = models.CharField(max_length=100, choices=IDENTITY_TYPE, null=True, blank=True)
    identity_image = models.FileField(upload_to=user_directory_path, default="default.jpg", null=True, blank=True)
    
    # Social account links
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)

    wallet = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    verified = models.BooleanField(default=False)

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Order profiles by descending dates
        ordering = ['-date']
    
    def __str__(self):
        if self.full_name:
            return f"{self.full_name}"  # Return full name if available
        else:
            return f"{self.user.username}"  # Otherwise, use username


# Signal handlers to create and save Profile objects upon User creation
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Connect the signal handlers to the User model
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
