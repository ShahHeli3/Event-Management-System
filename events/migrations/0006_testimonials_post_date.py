# Generated by Django 4.0.5 on 2022-06-14 07:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_alter_testimonials_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonials',
            name='post_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
