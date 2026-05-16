from django.db import models
import uuid
from cloudinary.models import CloudinaryField

class Property(models.Model):
    # Status choices
    STATUS_CHOICES = [
        ('For Sale', 'For Sale'),
        ('For Rent', 'For Rent'),
    ]

    # Property Type choices
    TYPE_CHOICES = [
        ('Apartment', 'Apartment'),
        ('Villa', 'Villa'),
        ('Plot', 'Plot'),
        ('Commercial', 'Commercial'),
    ]

    # Area choices
    AREA_CHOICES = [
        ('Pune', 'Pune'),
        ('PCMC', 'PCMC'),
    ]

    # Furnishing choices
    FURNISHING_CHOICES = [
        ('Unfurnished', 'Unfurnished'),
        ('Semi-furnished', 'Semi-furnished'),
        ('Fully-furnished', 'Fully-furnished'),
    ]

    # Facing choices
    FACING_CHOICES = [
        ('East', 'East'),
        ('West', 'West'),
        ('North', 'North'),
        ('South', 'South'),
        ('North-East', 'North-East'),
        ('North-West', 'North-West'),
        ('South-East', 'South-East'),
        ('South-West', 'South-West'),
    ]

    # 1. CORE DETAILS
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price_display = models.CharField(max_length=50, help_text="e.g. ₹1.2 Cr or ₹35,000 / mo")
    price_amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Numeric price for sorting/filtering")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='For Sale')
    property_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Apartment')
    
    # 2. LOCATION
    location = models.CharField(max_length=100, help_text="Specific area like Baner, Wakad")
    area = models.CharField(max_length=20, choices=AREA_CHOICES, default='Pune')
    address = models.TextField(blank=True, null=True)
    landmark = models.CharField(max_length=100, blank=True, null=True)

    # 3. SPECIFICATIONS
    bhk = models.IntegerField(default=2)
    bathrooms = models.IntegerField(default=2)
    sqft = models.IntegerField(help_text="Total area in square feet")
    furnishing_status = models.CharField(max_length=30, choices=FURNISHING_CHOICES, default='Unfurnished')
    facing = models.CharField(max_length=20, choices=FACING_CHOICES, blank=True, null=True)
    property_age = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. 0-5 years, Ready to move")
    floor_number = models.IntegerField(blank=True, null=True)
    total_floors = models.IntegerField(blank=True, null=True)

    # 4. AMENITIES (Booleans)
    has_parking = models.BooleanField(default=False)
    has_lift = models.BooleanField(default=False)
    has_power_backup = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_security = models.BooleanField(default=False)
    has_swimming_pool = models.BooleanField(default=False)

    # 5. LISTER INFORMATION (Internal/Contact)
    lister_name = models.CharField(max_length=100)
    lister_phone = models.CharField(max_length=15)
    lister_role = models.CharField(max_length=50, default='Owner', help_text="Owner, Agent, etc.")
    
    # 6. SYSTEM FIELDS
    main_image = CloudinaryField('image', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.location} ({'Approved' if self.is_approved else 'Pending'})"

    class Meta:
        verbose_name_plural = "Properties"

class PropertyImage(models.Model):
    CATEGORY_CHOICES = [
        ('Hero', 'Main Photo'),
        ('Interior', 'Interior (Living/Bed/Kitchen)'),
        ('Exterior', 'Exterior (Building/Front)'),
        ('Amenities', 'Amenities (Gym/Pool/Garden)'),
        ('Map', 'Layout / Map'),
        ('Neighborhood', 'Neighborhood / Surroundings'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='Interior')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"Image for {self.property.title} - {self.category}"

class Inquiry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='inquiries')
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField()
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Closed', 'Closed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Inquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"Inquiry from {self.full_name} for {self.property.title if self.property else 'General'}"
