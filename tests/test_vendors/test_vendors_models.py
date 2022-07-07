from rest_framework.test import APITestCase

from accounts.models import User
from vendors.models import VendorCategories, VendorImages, VendorRegistration


class TestModels(APITestCase):
    """
    class to test models of vendors app
    """
    def setUp(self):

        self.vendor_category = 'Test vendor category'

        # create object for VendorCategories model
        self.create_vendor_category = VendorCategories.objects.create(vendor_category=self.vendor_category)

        self.user = User.objects.create(email='heli@gmail.com', username='heli', first_name='Heli', last_name='Shah',
                                        contact_number='+919876543210', is_event_manager=True)
        self.vendor_details = 'Test vendor details'

        # create object for VendorRegistration model
        self.create_vendor = VendorRegistration.objects.create(user=self.user,
                                                               vendor_category=self.create_vendor_category,
                                                               vendor_details=self.vendor_details)

        with open('media/default.jpg') as image:
            self.vendor_image = image.name

        self.vendor_image_title = 'Test vendor image title'
        self.vendor_image_details = 'Test vendor image details'

        # create object for VendorImages model
        self.create_vendor_image = VendorImages.objects.create(vendor=self.create_vendor,
                                                               vendor_image=self.vendor_image,
                                                               vendor_image_title=self.vendor_image_title,
                                                               vendor_image_details=self.vendor_image_details)

    def test_vendor_categories_model(self):
        """
        function to test if the vendor categories model functions correctly
        """
        self.assertEqual(self.create_vendor_category.vendor_category, self.vendor_category)

    def test_vendor_registration_model(self):
        """
        function to test if the vendor registration model functions correctly
        """
        self.assertEqual(self.create_vendor.user, self.user)
        self.assertEqual(self.create_vendor.vendor_category, self.create_vendor_category)
        self.assertEqual(self.create_vendor.vendor_details, self.vendor_details)

    def test_vendor_images_model(self):
        """
        function to test if the vendor images model functions correctly
        """
        self.assertEqual(self.create_vendor_image.vendor, self.create_vendor)
        self.assertEqual(self.create_vendor_image.vendor_image, self.vendor_image)
        self.assertEqual(self.create_vendor_image.vendor_image_title, self.vendor_image_title)
        self.assertEqual(self.create_vendor_image.vendor_image_details, self.vendor_image_details)
