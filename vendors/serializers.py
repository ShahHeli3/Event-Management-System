from rest_framework import serializers

from accounts.models import User
from events.utils import Util
from .models import VendorCategories, VendorRegistration, VendorImages


class VendorCategoriesSerializer(serializers.ModelSerializer):
    """
    serializer for vendor categories
    """
    class Meta:
        model = VendorCategories
        fields = ['vendor_category']


class VendorRegistrationSerializer(serializers.ModelSerializer):
    """
    serializer for vendor registration
    """
    class Meta:
        model = VendorRegistration
        fields = ['vendor_category', 'vendor_details', 'user']

    def validate(self, attrs):
        """
        sends an email to all the event managers that a new vendor has sent a registration request
        """
        managers = User.objects.filter(is_event_manager=True)
        managers_email = [i.email for i in managers]

        data = self.context.get('data')
        user = self.context.get('user')

        # send mail to all the event managers that a new question has been posted
        body = "User ID : " + str(data['user']) + "\nUsername : " + str(user) + "\nVendor Category : " + \
               str(data['vendor_category']) + "\nVendor Details : " + str(data['vendor_details'])

        data = {
            'subject': 'New Vendor Registration',
            'body': body,
            'to_email': managers_email
        }
        Util.send_mail(data)
        return attrs


class ApproveVendorSerializer(serializers.ModelSerializer):
    """
    serializer for event managers to approve vendors
    """
    class Meta:
        model = VendorRegistration
        fields = ['is_approved']

    def validate(self, attrs):
        email = self.context.get('email')
        is_approved = attrs.get('is_approved')

        if is_approved:
            body = "Congratulations! Your vendor request has been approved."
            subject = "Vendor Request Approval"

        else:
            body = "Sorry! Your vendor request has been rejected."
            subject = "Vendor Request Rejection"

        data = {
            'subject': subject,
            'body': body,
            'to_email': [email]
        }
        Util.send_mail(data)
        return attrs


class VendorUpdateSerializer(serializers.ModelSerializer):
    """
    serializer to update vendor details
    """
    class Meta:
        model = VendorRegistration
        fields = ['vendor_details']


class GetVendorUserDetails(serializers.ModelSerializer):
    """
    serializer to get vendor's personal information
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'contact_number', 'profile_image']


class GetVendorImagesSerializer(serializers.ModelSerializer):
    """
    serializer to get vendor images
    """
    class Meta:
        model = VendorImages
        fields = ['vendor_image_title', 'vendor_image', 'vendor_image_details']


class GetVendorDetailsSerializer(serializers.ModelSerializer):
    """
    serializer to get vendor details
    """

    user_details = serializers.SerializerMethodField(read_only=True)

    def get_user_details(self, obj):
        user_details = User.objects.filter(username=obj)
        return GetVendorUserDetails(user_details, many=True).data

    image_set = GetVendorImagesSerializer(many=True, read_only=True)

    class Meta:
        model = VendorRegistration
        fields = ['user_details', 'vendor_details', 'image_set']


class VendorImageSerializer(serializers.ModelSerializer):
    """
    serializer for vendor images
    """
    class Meta:
        model = VendorImages
        fields = '__all__'
