from rest_framework.test import APISimpleTestCase
from django.urls import reverse, resolve

from vendors.views import GetVendorCategoriesView, VendorCategoriesViewSet, VendorRegistrationView, ApproveVendorView, \
    VendorDetails, VendorImageView, GetVendorInformationView, GetAllVendors


class TestUrls(APISimpleTestCase):
    """
    class to test all the urls of vendors app
    """

    def check_urls(self, url, view):
        """
        function to test if the given url matches with its view
        :param url: url to be tested
        :param view: view connected to the url
        """
        self.assertEqual(resolve(url).func.view_class, view)

    def test_vendor_categories_list_router(self):
        """
        to test if the router for get and post vendor categories works
        """
        self.assertEqual(resolve(reverse('vendor_categories-list')).func.cls, VendorCategoriesViewSet)

    def test_vendor_categories_detail_router(self):
        """
        to test if the router for update and delete vendor categories works
        """
        self.assertEqual(resolve(reverse('vendor_categories-detail', kwargs={'pk': 1})).func.cls,
                         VendorCategoriesViewSet)

    def test_view_vendor_categories_url(self):
        """
        to test if url to view_vendor_categories works
        """
        self.check_urls(reverse('view_vendor_categories'), GetVendorCategoriesView)

    def test_vendor_registration_url(self):
        """
        to test if url to vendor_registration works
        """
        self.check_urls(reverse('vendor_registration'), VendorRegistrationView)

    def test_approve_vendor_url(self):
        """
        to test if url to approve_vendor works
        """
        self.check_urls(reverse('approve_vendor', kwargs={'id': 1}), ApproveVendorView)

    def test_vendor_details_url(self):
        """
        to test if url to vendor_details works
        """
        self.check_urls(reverse('vendor_details', kwargs={'id': 1}), VendorDetails)

    def test_add_vendor_images_url(self):
        """
        to test if url to add_vendor_images works
        """
        self.check_urls(reverse('add_vendor_images'), VendorImageView)

    def test_vendor_images_url(self):
        """
        to test if url to vendor_images works
        """
        self.check_urls(reverse('vendor_images', kwargs={'id': 1}), VendorImageView)

    def test_vendor_information_url(self):
        """
        to test if url to vendor_information works
        """
        self.check_urls(reverse('vendor_information', kwargs={'id': 1}), GetVendorInformationView)

    def test_vendors_url(self):
        """
        to test if url to vendors works
        """
        self.check_urls(reverse('vendors'), GetAllVendors)
