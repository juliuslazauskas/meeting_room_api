from django.contrib.auth.models import User
from rest_framework import serializers
from book.models import Meeting_room, Booking
from django.contrib.auth.hashers import make_password
from django.db.models import Q


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """define a serializer for User model"""

    class Meta:
        model = User
        fields = [
            'url', 'username', 'email', 'first_name', 'last_name',
            'password']
        # fields must not be blank, password field will not be visible,
        # but can be updated by user, together with other fields
        extra_kwargs = {
            'username': {'required': True}, 'email': {'required': True},
            'first_name': {'required': True}, 'last_name': {'required': True},
            'password': {'write_only': True, 'required': True}}

    # custom update method needed because of password hashing.
    # standard method would just store password string as is in the db
    def update(self, instance, data):
        data["password"] = make_password(data["password"])
        return super().update(instance, data)


class UserAdminSerializer(UserSerializer):
    """User serializer extension for 'is_staff' users,
        adding additional field
    """

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ['is_staff']
        extra_kwargs = UserSerializer.Meta.extra_kwargs

    # custom create method to allow hashed password to be set for user
    # and password hash will be saved in db
    def create(self, data):
        user = super().create(data)
        user.set_password(data['password'])
        user.save()
        return user


class Meeting_roomSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for meeting rooms"""

    # additional field to store the owner - user that creats meeting room
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Meeting_room
        fields = ['url', 'owner', 'name', 'location']
        # fields must not be blank
        extra_kwargs = {'name': {'required': True},
                        'location': {'required': True}}

    # validate input if meeting room with same parameters exist
    def validate(self, data):
        qs = Meeting_room.objects.filter(name=data['name'],
                                         location=data['location'])
        if qs.exists():
            raise serializers.ValidationError("Room already exists. Name and \
location must be unique.")
        return data


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for room reservations"""

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Booking
        fields = ['url', 'owner', 'title', 'booked_from', 'booked_to',
                  'room_booked']
        # fields must not be blank
        extra_kwargs = {'title': {'required': True},
                        'booked_from': {'required': True},
                        'booked_to': {'required': True}
                        }

    # validate input for double booking and logic for start/end
    def validate(self, data):
        if data['booked_from'] > data['booked_to']:
            raise serializers.ValidationError("Booking end time must be \
after booking start time")
        qs = Booking.objects.filter(
            Q(booked_from__lte=data['booked_from'],
              booked_to__gte=data['booked_from'])
            | Q(booked_from__lte=data['booked_to'],
                booked_to__gte=data['booked_to']),
            room_booked=data['room_booked'])
        if qs.exists():
            raise serializers.ValidationError("The meeting room is occupied \
at the selected time")
        return data
