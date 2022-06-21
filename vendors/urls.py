from django.urls import path
from rest_framework.routers import DefaultRouter

from vendors.views import GetVendorCategoriesView, VendorCategoriesViewSet, VendorRegistrationView, ApproveVendorView, \
    VendorDetails, VendorImageView, GetVendorInformationView, GetAllVendors

router = DefaultRouter()
router.register('vendor_categories', VendorCategoriesViewSet, basename='vendor_categories')

urlpatterns = [
    path('view_vendor_categories/', GetVendorCategoriesView.as_view(), name='view_vendor_categories'),
    path('vendor_registration/', VendorRegistrationView.as_view(), name='vendor_registration'),
    path('approve_vendor/<int:id>/', ApproveVendorView.as_view(), name='approve_vendor'),
    path('vendor_details/<int:id>/', VendorDetails.as_view(), name='vendor_details'),
    path('add_vendor_images/', VendorImageView.as_view(), name='add_vendor_images'),
    path('vendor_images/<int:id>/', VendorImageView.as_view(), name='vendor_images'),
    path('vendor_information/<int:id>/', GetVendorInformationView.as_view(), name='vendor_information'),
    path('vendors/', GetAllVendors.as_view(), name='vendors'),
] + router.urls
