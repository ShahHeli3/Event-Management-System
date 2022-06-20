from django.contrib import admin

from vendors.models import VendorCategories, VendorRegistration, VendorImages

admin.site.register(VendorCategories)
admin.site.register(VendorRegistration)
admin.site.register(VendorImages)
