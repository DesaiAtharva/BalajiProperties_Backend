import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from properties.models import Property

def seed():
    properties_data = [
        {
            'title': 'Luxury 3 BHK Apartment in Baner',
            'price_display': '₹1.45 Cr',
            'location': 'Baner',
            'area': 'Pune',
            'property_type': 'Apartment',
            'bhk': 3,
            'bathrooms': 3,
            'sqft': 1650,
            'main_image': 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=800',
            'status': 'For Sale',
            'is_approved': True,
            'is_featured': True,
        },
        {
            'title': 'Premium 2 BHK near Wakad Center',
            'price_display': '₹82 L',
            'location': 'Wakad',
            'area': 'PCMC',
            'property_type': 'Apartment',
            'bhk': 2,
            'bathrooms': 2,
            'sqft': 1100,
            'main_image': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&q=80&w=800',
            'status': 'For Sale',
            'is_approved': True,
            'is_featured': True,
        },
        {
            'title': 'Modern 4 BHK Villa in Kothrud',
            'price_display': '₹4.2 Cr',
            'location': 'Kothrud',
            'area': 'Pune',
            'property_type': 'Villa',
            'bhk': 4,
            'bathrooms': 4,
            'sqft': 3200,
            'main_image': 'https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&q=80&w=800',
            'status': 'For Sale',
            'is_approved': True,
            'is_featured': True,
        },
        {
            'title': 'Spacious 2 BHK for Rent in Hinjewadi Ph 1',
            'price_display': '₹32,000 / mo',
            'location': 'Hinjewadi',
            'area': 'Pune',
            'property_type': 'Apartment',
            'bhk': 2,
            'bathrooms': 2,
            'sqft': 1150,
            'main_image': 'https://images.unsplash.com/photo-1493809842364-78817add7ffb?auto=format&fit=crop&q=80&w=800',
            'status': 'For Rent',
            'is_approved': True,
            'is_featured': True,
        },
        {
            'title': 'Residential Plot in Ravet (Pradhikaran)',
            'price_display': '₹75 L',
            'location': 'Ravet',
            'area': 'PCMC',
            'property_type': 'Plot',
            'bhk': 0,
            'bathrooms': 0,
            'sqft': 2200,
            'main_image': 'https://images.unsplash.com/photo-1524230659092-dc20b01227a1?auto=format&fit=crop&q=80&w=800',
            'status': 'For Sale',
            'is_approved': True,
            'is_featured': True,
        },
        {
            'title': 'Commercial Office Space in Viman Nagar',
            'price_display': '₹2.5 Cr',
            'location': 'Viman Nagar',
            'area': 'Pune',
            'property_type': 'Commercial',
            'bhk': 0,
            'bathrooms': 2,
            'sqft': 1400,
            'main_image': 'https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&q=80&w=800',
            'status': 'For Sale',
            'is_approved': True,
            'is_featured': True,
        },
        {
            'title': 'Elegant 3 BHK in Balewadi High Street',
            'price_display': '₹1.85 Cr',
            'location': 'Balewadi',
            'area': 'Pune',
            'property_type': 'Apartment',
            'bhk': 3,
            'bathrooms': 3,
            'sqft': 1800,
            'main_image': 'https://images.unsplash.com/photo-1512918766673-cd8085d34191?auto=format&fit=crop&q=80&w=800',
            'status': 'For Sale',
            'is_approved': True,
            'is_featured': False,
        },
        {
            'title': 'Affordable 1 BHK in Ravet',
            'price_display': '₹45 L',
            'location': 'Ravet',
            'area': 'PCMC',
            'property_type': 'Apartment',
            'bhk': 1,
            'bathrooms': 1,
            'sqft': 650,
            'main_image': 'https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&q=80&w=800',
            'status': 'For Sale',
            'is_approved': True,
            'is_featured': False,
        }
    ]

    for data in properties_data:
        Property.objects.get_or_create(
            title=data['title'],
            defaults=data
        )
    print("Successfully seeded property data!")

if __name__ == '__main__':
    seed()
