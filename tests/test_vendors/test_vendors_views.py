from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import User
from vendors.models import VendorCategories, VendorRegistration, VendorImages


class TestViews(APITestCase):
    """
    class to test views of vendors app
    """
    def setUp(self):
        self.admin_user = User.objects.create_user(email='admin@gmail.com', username='admin', first_name='Test',
                                                   last_name='Data', password='Abc@1234',
                                                   contact_number='+919876543210', is_event_manager=True)

        self.normal_user = User.objects.create_user(email='heli@gmail.com', username='heli', first_name='Heli',
                                                    last_name='Shah', password='Abc@1234',
                                                    contact_number='+919876543211', is_event_manager=False)

        self.create_vendor_category = VendorCategories.objects.create(vendor_category='Test Vendor Category')
        self.vendor_category_id = self.create_vendor_category.id

        self.create_vendor = VendorRegistration.objects.create(user=self.normal_user,
                                                               vendor_category=self.create_vendor_category,
                                                               vendor_details='Test vendor details',
                                                               is_approved=True)
        self.vendor_id = self.create_vendor.id

        with open('media/default.jpg') as image:
            self.vendor_image = image.name

        self.create_vendor_image = VendorImages.objects.create(vendor=self.create_vendor,
                                                               vendor_image=self.vendor_image,
                                                               vendor_image_title='Test vendor image title',
                                                               vendor_image_details='Test vendor image details')
        self.vendor_image_id = self.create_vendor_image.id

    def test_get_vendor_categories_successful(self):
        """
        function to test that vendor categories can be viewed successfully
        """
        response = self.client.get(reverse('view_vendor_categories'))
        self.assertEqual(response.status_code, 200)

    def test_post_vendor_category_fails_if_unauthorized(self):
        """
        vendor category cannot be added if user is unauthorized
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        response = self.client.post(reverse('vendor_categories-list'), {'vendor_category': 'Test vendor category'},
                                    format='json')
        self.assertEqual(response.status_code, 403)

    def test_post_vendor_category_successful(self):
        """
        only event managers(admin users) can add a new vendor category
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

        response = self.client.post(reverse('vendor_categories-list'), {'vendor_category': 'Test vendor category'},
                                    format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_vendor_category_fails_if_unauthorized(self):
        """
        unauthorized user cannot update any vendor category
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        vendor_category = VendorCategories.objects.get(id=self.vendor_category_id).id
        response = self.client.put(reverse('vendor_categories-detail', kwargs={'pk': vendor_category}),
                                    {'vendor_category': 'Test vendor category'}, format='json')
        self.assertEqual(response.status_code, 403)

    def test_update_vendor_category_successful(self):
        """
        only event managers(admin users) can update vendor category
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

        vendor_category = VendorCategories.objects.get(id=self.vendor_category_id).id
        response = self.client.put(reverse('vendor_categories-detail', kwargs={'pk': vendor_category}),
                                    {'vendor_category': 'Test vendor category'}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_vendor_category_fails_if_unauthorized(self):
        """
        unauthorized user cannot delete any vendor category
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        vendor_category = VendorCategories.objects.get(id=self.vendor_category_id).id

        response = self.client.delete(reverse('vendor_categories-detail', kwargs={'pk': vendor_category}))
        self.assertEqual(response.status_code, 403)

    def test_delete_vendor_category_successful(self):
        """
        only event managers(admin users) can delete vendor category
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

        vendor_category = VendorCategories.objects.get(id=self.vendor_category_id).id

        response = self.client.delete(reverse('vendor_categories-detail', kwargs={'pk': vendor_category}))
        self.assertEqual(response.status_code, 204)

    def test_vendor_registration_fails_if_unauthenticated(self):
        """
        user cannot register as a vendor if not authenticated
        """
        response = self.client.post(reverse('vendor_registration'))
        self.assertEqual(response.status_code, 401)

    def test_vendor_registration_successful(self):
        """
        user can register as a vendor if authenticated and provides valid data
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        vendor_category = VendorCategories.objects.get(id=self.vendor_category_id).id

        response = self.client.post(reverse('vendor_registration'), {'vendor_category': vendor_category,
                                                                     'vendor_details': 'Test vendor details',
                                                                     }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_vendor_approve_fails_if_unauthorized(self):
        """
        unauthorized user cannot approve a vendor
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        vendor = VendorRegistration.objects.get(id=self.vendor_id).id

        response = self.client.put(reverse('approve_vendor', kwargs={'id': vendor}), {'is_approved': False},
                                   format='json')
        self.assertEqual(response.status_code, 403)

    def test_vendor_approve_successful(self):
        """
        only event managers(admin users) can approve a vendor
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

        vendor = VendorRegistration.objects.get(id=self.vendor_id).id

        response = self.client.put(reverse('approve_vendor', kwargs={'id': vendor}), {'is_approved': False},
                                   format='json')
        self.assertEqual(response.status_code, 200)

    def test_vendor_details_update_fails_if_unauthorized(self):
        """
        unauthorized user cannot update a vendor's details
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

        vendor = VendorRegistration.objects.get(id=self.vendor_id).id

        response = self.client.put(reverse('vendor_details', kwargs={'id': vendor}))
        self.assertEqual(response.status_code, 400)

    def test_vendor_details_update_successful(self):
        """
        a user himself can update his own vendor details
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        vendor = VendorRegistration.objects.get(id=self.vendor_id).id

        response = self.client.put(reverse('vendor_details', kwargs={'id': vendor}), {'vendor_details': 'Test update'},
                                   format='json')
        self.assertEqual(response.status_code, 200)

    def test_vendor_delete_fails_if_unauthorized(self):
        """
        unauthorized user cannot delete a vendor
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

        vendor = VendorRegistration.objects.get(id=self.vendor_id).id

        response = self.client.delete(reverse('vendor_details', kwargs={'id': vendor}))
        self.assertEqual(response.status_code, 400)

    def test_vendor_delete_successful(self):
        """
        a user himself can delete his own vendor profile
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        vendor = VendorRegistration.objects.get(id=self.vendor_id).id

        response = self.client.delete(reverse('vendor_details', kwargs={'id': vendor}))
        self.assertEqual(response.status_code, 204)

    def test_add_vendor_images_fails_if_wrong_format(self):
        """
        image files other than .jpg, .png and .jpeg cannot be added
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

        vendor = VendorRegistration.objects.get(id=self.vendor_id).id
        image_data = File(open('requirements.txt', 'rb'))
        image = SimpleUploadedFile('image.jpg', image_data.read(), content_type='multipart/form-data')

        response = self.client.post(reverse('add_vendor_images'), {'vendor': vendor,
                                                                   'vendor_image': image,
                                                                   'vendor_image_title': 'Test vendor image title',
                                                                   'vendor_image_details': 'Test vendor image details'},
                                    format='multipart')

        self.assertEqual(response.status_code, 400)

    def test_add_vendor_images_successful(self):
        """
        vendors can add images to their profile
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        vendor = VendorRegistration.objects.get(id=self.vendor_id).id
        image_data = File(open('media/default.jpg', 'rb'))
        image = SimpleUploadedFile('image.jpg', image_data.read(), content_type='multipart/form-data')

        response = self.client.post(reverse('add_vendor_images'), {'vendor': vendor,
                                                                   'vendor_image': image,
                                                                   'vendor_image_title': 'Test vendor image title',
                                                                   'vendor_image_details': 'Test vendor image details'},
                                    format='multipart')

        self.assertEqual(response.status_code, 201)

    def test_cannot_update_vendor_images_if_unauthorized(self):
        """
        unauthorized users cannot update other vendor's images
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

        vendor_image = VendorImages.objects.get(id=self.vendor_image_id).id
        image_data = File(open('media/default.jpg', 'rb'))
        image = SimpleUploadedFile('image.jpg', image_data.read(), content_type='multipart/form-data')

        response = self.client.put(reverse('vendor_images', kwargs={'id': vendor_image}),
                                   {'vendor_image': image,
                                    'vendor_image_title': 'Test vendor image title',
                                    'vendor_image_details': 'Test vendor image details'}, format='multipart')

        self.assertEqual(response.status_code, 400)

    def test_update_event_images_fails_if_wrong_format(self):
        """
        images cannot be updated/replaced with files other than .jpg, .jpeg and .png formats
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        vendor_image = VendorImages.objects.get(id=self.vendor_image_id).id
        image_data = File(open('requirements.txt', 'rb'))
        image = SimpleUploadedFile('image.jpg', image_data.read(), content_type='multipart/form-data')

        response = self.client.put(reverse('vendor_images', kwargs={'id': vendor_image}),
                                   {'vendor_image': image,
                                    'vendor_image_title': 'Test vendor image title',
                                    'vendor_image_details': 'Test vendor image details'}, format='multipart')

        self.assertEqual(response.status_code, 400)

    def test_update_event_images_successful(self):
        """
        images can only be updated by the vendor himself
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        vendor_image = VendorImages.objects.get(id=self.vendor_image_id).id
        image_data = File(open('media/default.jpg', 'rb'))
        image = SimpleUploadedFile('image.jpg', image_data.read(), content_type='multipart/form-data')

        response = self.client.put(reverse('vendor_images', kwargs={'id': vendor_image}),
                                   {'vendor_image': image,
                                    'vendor_image_title': 'Test vendor image title',
                                    'vendor_image_details': 'Test vendor image details'}, format='multipart')

        self.assertEqual(response.status_code, 200)

    def test_cannot_delete_vendor_images_if_unauthorized(self):
        """
        unauthorized users cannot delete other vendor's images
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

        vendor_image = VendorImages.objects.get(id=self.vendor_image_id).id

        response = self.client.delete(reverse('vendor_images', kwargs={'id': vendor_image}))

        self.assertEqual(response.status_code, 400)

    def test_delete_event_images_successful(self):
        """
        images can only be deleted by the vendor himself
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        vendor_image = VendorImages.objects.get(id=self.vendor_image_id).id

        response = self.client.delete(reverse('vendor_images', kwargs={'id': vendor_image}))

        self.assertEqual(response.status_code, 204)

    def test_get_vendor_information_fails_if_unauthenticated(self):
        """
        unauthorized users cannot view vendors' information
        """
        vendor = VendorRegistration.objects.get(pk=self.vendor_id).id

        response = self.client.get(reverse('vendor_information', kwargs={'id': vendor}))
        self.assertEqual(response.status_code, 401)

    def test_get_vendor_information_successful(self):
        """
        authorized users cannot view vendors' information
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        vendor = VendorRegistration.objects.get(pk=self.vendor_id).id

        response = self.client.get(reverse('vendor_information', kwargs={'id': vendor}))
        self.assertEqual(response.status_code, 200)

    def test_get_all_vendors_fails_if_unauthenticated(self):
        """
        unauthorized users cannot view vendors
        """
        response = self.client.get(reverse('vendors'))
        self.assertEqual(response.status_code, 401)

    def test_get_all_vendors_successful(self):
        """
        authorized users cannot view vendors' information
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse('vendors'))
        self.assertEqual(response.status_code, 200)
