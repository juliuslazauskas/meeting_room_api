# Generated by Django 3.1.5 on 2021-03-08 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User_booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=150)),
                ('email', models.CharField(default='', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting_room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=150)),
                ('booked_from', models.DateTimeField()),
                ('booked_to', models.DateTimeField()),
                ('user_booked', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.user_booking')),
            ],
        ),
    ]
