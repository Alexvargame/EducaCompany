# Generated by Django 4.2.5 on 2023-11-14 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educa', '0019_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
