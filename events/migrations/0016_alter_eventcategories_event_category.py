# Generated by Django 4.0.5 on 2022-06-17 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_eventimages_event_image_details_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventcategories',
            name='event_category',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
