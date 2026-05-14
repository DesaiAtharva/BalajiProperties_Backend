from django.urls import path
from .views import (
    PropertyListAPIView, PropertyDetailAPIView, PropertyCreateAPIView, 
    InquiryCreateAPIView, AdminPropertyListAPIView, AdminPropertyActionAPIView, 
    AdminInquiryListAPIView, AdminPropertyUpdateAPIView, AdminInquiryActionAPIView,
    AdminLoginAPIView
)

urlpatterns = [
    path('admin/login/', AdminLoginAPIView.as_view(), name='admin-login'),
    path('properties/', PropertyListAPIView.as_view(), name='property-list'),
    path('properties/<uuid:id>/', PropertyDetailAPIView.as_view(), name='property-detail'),
    path('properties/submit/', PropertyCreateAPIView.as_view(), name='property-submit'),
    path('inquiries/submit/', InquiryCreateAPIView.as_view(), name='inquiry-submit'),
    
    # Admin APIs
    path('admin/properties/', AdminPropertyListAPIView.as_view(), name='admin-property-list'),
    path('admin/properties/<uuid:id>/action/', AdminPropertyActionAPIView.as_view(), name='admin-property-action'),
    path('admin/properties/<uuid:id>/update/', AdminPropertyUpdateAPIView.as_view(), name='admin-property-update'),
    path('admin/inquiries/', AdminInquiryListAPIView.as_view(), name='admin-inquiry-list'),
    path('admin/inquiries/<uuid:id>/action/', AdminInquiryActionAPIView.as_view(), name='admin-inquiry-action'),
]
