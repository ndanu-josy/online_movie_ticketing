# Generated by Django 3.2.5 on 2021-07-27 18:10

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Theatre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Waves Cinema', max_length=50)),
                ('city', models.CharField(choices=[('NAIROBI', 'nairobi'), ('KISUMU', 'Kisumu'), ('MOMBASA', 'Mombasa')], max_length=20)),
                ('address', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('poster', cloudinary.models.CloudinaryField(max_length=255, verbose_name='imageposter')),
                ('description', models.CharField(max_length=500)),
                ('theatre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.theatre')),
            ],
        ),
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('hall_type', models.CharField(choices=[('2D', '2D'), ('3D', '3D'), ('4DX', '4DX'), ('IMAX', 'IMAX')], max_length=4)),
                ('theatre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.theatre')),
            ],
        ),
    ]
