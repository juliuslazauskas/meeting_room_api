# Generated by Django 3.1.5 on 2021-03-08 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting_room',
            name='booked_from',
        ),
        migrations.RemoveField(
            model_name='meeting_room',
            name='booked_to',
        ),
        migrations.RemoveField(
            model_name='meeting_room',
            name='user_booked',
        ),
        migrations.AddField(
            model_name='meeting_room',
            name='location',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booked_from', models.DateTimeField()),
                ('booked_to', models.DateTimeField()),
                ('room_booked', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.meeting_room')),
                ('user_booked', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.user_booking')),
            ],
        ),
    ]
