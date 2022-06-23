from django.db import models

from accounts.models import User


class VendorCategories(models.Model):
    """
    model for vendor categories
    """
    vendor_category = models.CharField(max_length=200, unique=True)


class VendorRegistration(models.Model):
    """
    model for vendor registration
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor_category = models.ForeignKey(VendorCategories, on_delete=models.CASCADE)
    vendor_details = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class VendorImages(models.Model):
    """
    model for vendor images
    """
    vendor = models.ForeignKey(VendorRegistration, on_delete=models.CASCADE, related_name='image_set')
    vendor_image = models.ImageField(upload_to="vendor_images/")
    vendor_image_title = models.CharField(max_length=200)
    vendor_image_details = models.TextField()

