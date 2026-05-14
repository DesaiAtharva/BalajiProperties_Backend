from rest_framework import serializers
from .models import Property, Inquiry

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        # For public listing, we might want to hide lister details or keep them
        # depending on user's preference. For now, we include them.
        fields = '__all__'

class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        # is_approved should not be set by the user during submission
        exclude = ('is_approved', 'is_featured')

class InquirySerializer(serializers.ModelSerializer):
    property_title = serializers.ReadOnlyField(source='property.title')
    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all(), required=False, allow_null=True)
    
    class Meta:
        model = Inquiry
        fields = '__all__'
