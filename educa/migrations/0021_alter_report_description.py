# Generated by Django 4.2.5 on 2023-11-14 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educa', '0020_alter_report_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='description',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
