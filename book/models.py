from django.db import models
from django.contrib.auth.models import User


class Meeting_room(models.Model):
    """creating meeting room model"""
    name = models.CharField(max_length=150, default='')
    location = models.CharField(max_length=150, default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default='')

    # class object representation by name field string
    def __str__(self):
        return self.name


class Booking(models.Model):
    """creating a booking model"""
    title = models.CharField(max_length=150, null=True)
    booked_from = models.DateTimeField()
    booked_to = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    room_booked = models.ForeignKey(Meeting_room, on_delete=models.CASCADE)

    # class object representation by name field string
    def __str__(self):
        return self.title
