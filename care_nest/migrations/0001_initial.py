# Generated by Django 5.2 on 2025-05-05 16:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('date_of_birth', models.DateField()),
                ('allergies', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('min_age', models.IntegerField()),
                ('max_age', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('enter_time', models.TimeField()),
                ('exit_time', models.TimeField()),
                ('status', models.CharField(choices=[('present', 'Present'), ('absent', 'Absent')], default='present', max_length=10)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='care_nest.child')),
            ],
        ),
        migrations.CreateModel(
            name='ChildAchievements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('achievement_type', models.CharField(choices=[('photo', 'Photo'), ('badge', 'Badge'), ('painting', 'Painting')], default='photo', max_length=10)),
                ('title', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=30)),
                ('image_url', models.CharField(max_length=255)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='care_nest.child')),
            ],
        ),
        migrations.AddField(
            model_name='child',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='care_nest.section'),
        ),
    ]
