# Generated by Django 4.2.5 on 2023-11-06 08:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('educa', '0012_remove_test_base_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='internship',
            name='interns',
            field=models.ManyToManyField(blank=True, related_name='internship_joined', to=settings.AUTH_USER_MODEL),
        ),
    ]
