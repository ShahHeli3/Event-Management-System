# Generated by Django 4.0.5 on 2022-06-14 06:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0002_rename_username_testimonials_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimonials',
            name='user',
            field=models.ForeignKey(on_delete=models.SET('Anonymous User'), related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
