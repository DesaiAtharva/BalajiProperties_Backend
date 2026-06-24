from rest_framework import serializers
from .models import Property, Inquiry, PropertyImage

class PropertyImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = PropertyImage
        fields = ['id', 'url', 'category', 'order']

    def get_url(self, obj):
        if hasattr(obj.image, 'url'):
            return obj.image.url
        return str(obj.image)

class PropertySerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()
    images = PropertyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = '__all__'

    def get_main_image(self, obj):
        if not obj.main_image:
            return None
        if hasattr(obj.main_image, 'url'):
            return obj.main_image.url
        return str(obj.main_image)

class PropertyCreateSerializer(serializers.ModelSerializer):
    # For creation, we keep it simple so DRF can handle the upload
    class Meta:
        model = Property
        exclude = ('is_approved', 'is_featured')

class InquirySerializer(serializers.ModelSerializer):
    property_title = serializers.ReadOnlyField(source='property.title')
    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all(), required=False, allow_null=True)
    
    class Meta:
        model = Inquiry
        fields = '__all__'
