# Generated by Django 4.0.5 on 2022-06-17 10:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vendors', '0003_alter_vendorcategories_vendor_category'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VendorDetails',
            new_name='VendorRegistration',
        ),
    ]
