# Generated by Django 4.0.5 on 2022-06-16 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_events'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventIdeas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_idea', models.TextField()),
                ('event_city', models.CharField(max_length=100)),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.events')),
            ],
        ),
        migrations.CreateModel(
            name='EventImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_image', models.ImageField(upload_to='event_images/')),
                ('event_image_title', models.CharField(max_length=200)),
                ('event_image_details', models.TextField()),
                ('event_idea_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.eventideas')),
            ],
        ),
    ]
