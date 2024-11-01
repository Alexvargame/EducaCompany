# Generated by Django 4.2.5 on 2023-10-31 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('type', models.CharField(choices=[('theory', 'theory'), ('practic', 'practic')], max_length=50)),
                ('assesment', models.JSONField()),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Направление',
                'verbose_name_plural': 'Направления',
            },
        ),
        migrations.CreateModel(
            name='Kata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('base', models.CharField(max_length=1000)),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('base', models.JSONField()),
            ],
            options={
                'verbose_name': 'Тест',
                'verbose_name_plural': 'Тесты',
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('assesment', models.JSONField()),
                ('course', models.ManyToManyField(related_name='courses', to='educa.course')),
                ('kata', models.ManyToManyField(related_name='kata', to='educa.kata')),
                ('test', models.ManyToManyField(related_name='test', to='educa.test')),
            ],
            options={
                'verbose_name': 'Тема',
                'verbose_name_plural': 'Темы',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('director', models.CharField(max_length=500)),
                ('task', models.CharField(max_length=1000)),
                ('direction', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='projct_directions', to='educa.direction')),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекты',
            },
        ),
        migrations.CreateModel(
            name='InternShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('director', models.CharField(max_length=500)),
                ('assesment', models.JSONField()),
                ('direction', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='intern_directions', to='educa.direction')),
            ],
            options={
                'verbose_name': 'Интернатура',
                'verbose_name_plural': 'Интернатуры',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='internship',
            field=models.ManyToManyField(related_name='internships', to='educa.internship'),
        ),
    ]
