# Generated by Django 4.2.5 on 2023-11-12 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educa', '0016_remove_kata_theme_remove_test_theme_theme_kata_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='kata',
            name='solution',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='test',
            name='solution',
            field=models.CharField(default='', max_length=100),
        ),
    ]
