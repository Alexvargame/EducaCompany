# Generated by Django 4.2.5 on 2023-11-13 12:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('educa', '0017_kata_solution_test_solution'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='internshipers',
            field=models.ManyToManyField(blank=True, related_name='internshiper_joined', to=settings.AUTH_USER_MODEL),
        ),
    ]
