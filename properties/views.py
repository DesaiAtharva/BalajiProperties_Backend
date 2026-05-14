from rest_framework import generics, permissions, status, views
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Property, Inquiry
from .serializers import PropertySerializer, PropertyCreateSerializer, InquirySerializer

class PropertyListAPIView(generics.ListAPIView):
    """
    Public API to list ONLY approved properties.
    """
    serializer_class = PropertySerializer
    
    def get_queryset(self):
        queryset = Property.objects.filter(is_approved=True)
        
        # Advanced filtering logic
        area = self.request.query_params.get('area')
        prop_type = self.request.query_params.get('type')
        status = self.request.query_params.get('status')
        bhk = self.request.query_params.get('bhk')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if area:
            queryset = queryset.filter(area=area)
        if prop_type:
            queryset = queryset.filter(property_type=prop_type)
        if status:
            queryset = queryset.filter(status=status)
        if bhk:
            bhk_list = bhk.split(',')
            queryset = queryset.filter(bhk__in=bhk_list)
        if min_price:
            queryset = queryset.filter(price_amount__gte=min_price)
        if max_price:
            # If max_price is 500L (5Cr), we might want to treat it as "no upper limit"
            if int(float(max_price)) < 50000000:
                queryset = queryset.filter(price_amount__lte=max_price)
            
        return queryset

class PropertyDetailAPIView(generics.RetrieveAPIView):
    """
    Public API to view a single property.
    """
    queryset = Property.objects.filter(is_approved=True)
    serializer_class = PropertySerializer
    lookup_field = 'id'

class PropertyCreateAPIView(generics.CreateAPIView):
    """
    Public API for users to submit a property listing.
    Stored with is_approved=False by default.
    """
    queryset = Property.objects.all()
    serializer_class = PropertyCreateSerializer
    permission_classes = [permissions.AllowAny]

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class AdminLoginAPIView(ObtainAuthToken):
    """
    API for the Frontend Admin to login and get a Token.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user.is_staff:
            return Response({'error': 'Not an admin user'}, status=status.HTTP_403_FORBIDDEN)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })

from rest_framework.authentication import SessionAuthentication

class InquiryCreateAPIView(generics.CreateAPIView):
    """
    Public API for users to send an inquiry about a property.
    """
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [] # Disable session auth to avoid CSRF issues for public users

# --- ADMIN DASHBOARD APIS ---

class AdminPropertyListAPIView(generics.ListAPIView):
    """
    Private API for the Admin Dashboard to see ALL properties.
    """
    queryset = Property.objects.all().order_by('-created_at')
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAdminUser]

class AdminPropertyActionAPIView(views.APIView):
    """
    Private API to Approve or Delete properties from the Dashboard.
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, id):
        action = request.data.get('action') # 'approve' or 'delete'
        try:
            property = Property.objects.get(id=id)
            if action == 'approve':
                property.is_approved = not property.is_approved
                property.save()
                return Response({'status': 'updated', 'is_approved': property.is_approved})
            elif action == 'delete':
                property.delete()
                return Response({'status': 'deleted'})
        except Property.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)
        return Response({'error': 'Invalid action'}, status=400)

class AdminInquiryListAPIView(generics.ListAPIView):
    """
    Private API to see all customer inquiries.
    """
    queryset = Inquiry.objects.all().order_by('-created_at')
    serializer_class = InquirySerializer
    permission_classes = [permissions.IsAdminUser]

class AdminInquiryActionAPIView(views.APIView):
    """
    Private API to update the status of an inquiry.
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, id):
        new_status = request.data.get('status')
        try:
            inquiry = Inquiry.objects.get(id=id)
            if new_status in ['New', 'Contacted', 'Closed']:
                inquiry.status = new_status
                inquiry.save()
                return Response({'status': 'updated', 'current_status': inquiry.status})
        except Inquiry.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)
        return Response({'error': 'Invalid status'}, status=400)

class AdminPropertyUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Private API to Fetch and Update a specific property from the Dashboard.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'
