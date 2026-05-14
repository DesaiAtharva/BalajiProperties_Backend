from django.core.management.base import BaseCommand
from properties.models import Property
import re

class Command(BaseCommand):
    help = 'Seed initial properties from properties.ts'

    def handle(self, *args, **kwargs):
        existing_properties = [
            {
                'title': 'Luxury 3 BHK Apartment in Baner',
                'price': '₹1.45 Cr',
                'location': 'Baner',
                'area': 'Pune',
                'type': 'Apartment',
                'bhk': 3,
                'bathrooms': 3,
                'sqft': 1650,
                'image': 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=800',
                'status': 'For Sale',
                'featured': True,
            },
            {
                'title': 'Premium 2 BHK near Wakad Center',
                'price': '₹82 L',
                'location': 'Wakad',
                'area': 'PCMC',
                'type': 'Apartment',
                'bhk': 2,
                'bathrooms': 2,
                'sqft': 1100,
                'image': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&q=80&w=800',
                'status': 'For Sale',
                'featured': True,
            },
            {
                'title': 'Modern 4 BHK Villa in Kothrud',
                'price': '₹4.2 Cr',
                'location': 'Kothrud',
                'area': 'Pune',
                'type': 'Villa',
                'bhk': 4,
                'bathrooms': 4,
                'sqft': 3200,
                'image': 'https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&q=80&w=800',
                'status': 'For Sale',
                'featured': True,
            },
            {
                'title': 'Spacious 2 BHK for Rent in Hinjewadi Ph 1',
                'price': '₹32,000 / mo',
                'location': 'Hinjewadi',
                'area': 'Pune',
                'type': 'Apartment',
                'bhk': 2,
                'bathrooms': 2,
                'sqft': 1150,
                'image': 'https://images.unsplash.com/photo-1493809842364-78817add7ffb?auto=format&fit=crop&q=80&w=800',
                'status': 'For Rent',
                'featured': True,
            },
            {
                'title': 'Residential Plot in Ravet (Pradhikaran)',
                'price': '₹75 L',
                'location': 'Ravet',
                'area': 'PCMC',
                'type': 'Plot',
                'bhk': 0,
                'bathrooms': 0,
                'sqft': 2200,
                'image': 'https://images.unsplash.com/photo-1524230659092-dc20b01227a1?auto=format&fit=crop&q=80&w=800',
                'status': 'For Sale',
                'featured': True,
            },
            {
                'title': 'Commercial Office Space in Viman Nagar',
                'price': '₹2.5 Cr',
                'location': 'Viman Nagar',
                'area': 'Pune',
                'type': 'Commercial',
                'bhk': 0,
                'bathrooms': 2,
                'sqft': 1400,
                'image': 'https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&q=80&w=800',
                'status': 'For Sale',
                'featured': True,
            },
            {
                'title': 'Elegant 3 BHK in Balewadi High Street',
                'price': '₹1.85 Cr',
                'location': 'Balewadi',
                'area': 'Pune',
                'type': 'Apartment',
                'bhk': 3,
                'bathrooms': 3,
                'sqft': 1800,
                'image': 'https://images.unsplash.com/photo-1512918766673-cd8085d34191?auto=format&fit=crop&q=80&w=800',
                'status': 'For Sale',
                'featured': False,
            },
            {
                'title': 'Affordable 1 BHK in Ravet',
                'price': '₹45 L',
                'location': 'Ravet',
                'area': 'PCMC',
                'type': 'Apartment',
                'bhk': 1,
                'bathrooms': 1,
                'sqft': 650,
                'image': 'https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&q=80&w=800',
                'status': 'For Sale',
                'featured': False,
            }
        ]

        def parse_price(price_str):
            # Extract number
            numbers = re.findall(r"[-+]?\d*\.\d+|\d+", price_str.replace(',', ''))
            if not numbers: return 0
            val = float(numbers[0])
            
            if 'Cr' in price_str:
                return val * 10000000
            elif 'L' in price_str:
                return val * 100000
            return val

        for p_data in existing_properties:
            Property.objects.get_or_create(
                title=p_data['title'],
                defaults={
                    'price_display': p_data['price'],
                    'price_amount': parse_price(p_data['price']),
                    'location': p_data['location'],
                    'area': p_data['area'],
                    'property_type': p_data['type'],
                    'bhk': p_data['bhk'],
                    'bathrooms': p_data['bathrooms'],
                    'sqft': p_data['sqft'],
                    # We use the URL directly for image handling in this seed
                    'description': f"Beautiful {p_data['type']} located in {p_data['location']}.",
                    'status': p_data['status'],
                    'is_featured': p_data.get('featured', False),
                    'is_approved': True, # Seeded data is approved by default
                    'lister_name': 'Balaji Properties',
                    'lister_phone': '9890468329',
                    'lister_role': 'Admin'
                }
            )
            self.stdout.write(self.style.SUCCESS(f"Successfully seeded {p_data['title']}"))
