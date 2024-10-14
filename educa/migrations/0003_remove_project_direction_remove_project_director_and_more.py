# Generated by Django 4.2.5 on 2023-11-01 11:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('educa', '0002_remove_course_assesment_remove_internship_assesment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='direction',
        ),
        migrations.RemoveField(
            model_name='project',
            name='director',
        ),
        migrations.AddField(
            model_name='project',
            name='direction',
            field=models.ManyToManyField(related_name='projct_directions', to='educa.direction'),
        ),
        migrations.AddField(
            model_name='project',
            name='director',
            field=models.ManyToManyField(related_name='derectors', to=settings.AUTH_USER_MODEL),
        ),
    ]
