# Generated by Django 4.2.5 on 2023-11-07 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_profile_assesments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='assesments',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
