from django.contrib import admin
from .models import Property, Inquiry

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'property', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('full_name', 'phone_number', 'email', 'message')
    readonly_fields = ('created_at',)
from django.utils.html import format_html

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price_display', 'is_approved', 'is_featured', 'lister_name', 'lister_phone', 'created_at')
    list_filter = ('is_approved', 'is_featured', 'status', 'property_type', 'area')
    search_fields = ('title', 'location', 'lister_name', 'lister_phone')
    actions = ['approve_properties', 'unapprove_properties']
    
    # Organize fields in detail view
    fieldsets = (
        ('Approval Status', {
            'fields': ('is_approved', 'is_featured')
        }),
        ('Lister Contact (Internal)', {
            'fields': ('lister_name', 'lister_phone', 'lister_role')
        }),
        ('Core Details', {
            'fields': ('title', 'description', 'price_display', 'price_amount', 'status', 'property_type')
        }),
        ('Location', {
            'fields': ('location', 'area', 'address', 'landmark')
        }),
        ('Specifications', {
            'fields': ('bhk', 'bathrooms', 'sqft', 'furnishing_status', 'facing', 'property_age', 'floor_number', 'total_floors')
        }),
        ('Amenities', {
            'fields': ('has_parking', 'has_lift', 'has_power_backup', 'has_gym', 'has_security', 'has_swimming_pool')
        }),
        ('Media', {
            'fields': ('main_image',)
        }),
    )

    def approve_properties(self, request, queryset):
        queryset.update(is_approved=True)
    approve_properties.short_description = "Approve selected properties"

    def unapprove_properties(self, request, queryset):
        queryset.update(is_approved=False)
    unapprove_properties.short_description = "Mark selected properties as Pending"
