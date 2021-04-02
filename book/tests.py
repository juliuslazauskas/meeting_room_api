import pytz
from django.utils import timezone
from datetime import datetime, timedelta
from django.urls import include, path
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework.test import APIClient
from book.models import Meeting_room, Booking
from django.contrib import admin


class appTestCase(APITestCase, URLPatternsTestCase):

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('book.urls')),
    ]

    def setUp(self):
        '''Initialize test users and test data'''
        user = User.objects.create(
            username='testuser', email='mail@test.com',
            first_name='First_name', last_name='Last_name')
        staff_user = User.objects.create(
            username='teststaffuser', email='test@test.com',
            first_name='Staff_first_name', last_name='Staff_last_name',
            is_staff=True)
        user.set_password('pass123Word')
        staff_user.set_password('pass123Word')
        user.save()
        staff_user.save()
        staff_room = Meeting_room.objects.create(
            name='Room', location='Location', owner=staff_user
        )
        staff_meeting = Booking.objects.create(
            title='staff_meeting',
            booked_from=timezone.now() + timedelta(hours=1),
            booked_to=timezone.now() + timedelta(hours=2),
            owner=staff_user, room_booked=staff_room
        )

    def test_create_user(self):
        '''Check if 'is_staff' user can correctly create other users'''
        client = APIClient()
        self.client.login(username='teststaffuser', password='pass123Word')
        data = {'username': 'create_test', 'email': 'test@test.com',
                'first_name': 'U_first', 'last_name': 'U_last',
                'password': 'random_passW123', 'is_staff': 'false'}
        # creating a user
        response = self.client.post('/user_auth/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # check if fields match
        response = self.client.get('/user_auth/3/', format='json')
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['last_name'], data['last_name'])
        self.assertEqual(response.data['is_staff'],
                         (False if data['is_staff'] == 'false' else True))

    def test_create_user_f(self):
        '''Check if non 'is_staff" user cant create other users
        and can see only one user (himself) in the users view'''
        client = APIClient()
        username = 'testuser'
        password = 'pass123Word'
        self.client.login(username=username, password=password)
        data = {'username': 'create_test', 'email': 'test@test.com',
                'first_name': 'U_first', 'last_name': 'U_last',
                'password': 'random_passW123', 'is_staff': 'false'}
        # user fails to create other users
        response = self.client.post('/user_auth/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # user can see only himself
        response = self.client.get('/user_auth/', format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], username)

    def test_create_room(self):
        '''Check if non 'is_staff" user can create and delete his rooms,
           see all rooms, but can't delete other owner rooms'''
        client = APIClient()
        username = 'testuser'
        password = 'pass123Word'
        self.client.login(username=username, password=password)
        data = {'name': 'room_name1', 'location': 'somehwere1'}
        # user can create rooms
        response = self.client.post('/rooms/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # user can see all rooms
        response = self.client.get('/rooms/', format='json')
        self.assertEqual(len(response.data), 2)
        # user can delete rooms he owns
        response = self.client.delete('/rooms/2/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # user cant delete rooms he does not own
        response = self.client.delete('/rooms/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_meeting(self):
        '''Check if non 'is_staff" user can create and delete his meetings,
           see all meetings, but can't delete other owner meetings'''
        client = APIClient()
        username = 'testuser'
        password = 'pass123Word'
        time_from = timezone.now()
        time_to = time_from + timedelta(minutes=30)
        self.client.login(username=username, password=password)
        data = {'title': 'booking1', 'booked_from': time_from,
                'booked_to': time_to, 'room_booked': '/rooms/1/'}
        # user can do booking
        response = self.client.post('/bookings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # user can see his and other bookings
        response = self.client.get('/bookings/', format='json')
        self.assertEqual(len(response.data), 2)
        # user can delete his booking
        response = self.client.delete('/bookings/2/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # user cant delete bookings he does not own
        response = self.client.delete('/bookings/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_meeting_double_booking(self):
        '''Checks if double booking is possible'''
        client = APIClient()
        username = 'testuser'
        password = 'pass123Word'
        time_from = timezone.now()
        time_to = time_from + timedelta(minutes=59)
        self.client.login(username=username, password=password)
        data = {'title': 'booking1', 'booked_from': time_from,
                'booked_to': time_to, 'room_booked': '/rooms/1/'}
        # user can do booking till the staff meeting (created in setup)
        response = self.client.post('/bookings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # user can do booking after the staff meeting (created in setup)
        time_from = timezone.now() + timedelta(hours=2, minutes=1)
        time_to = time_from + timedelta(hours=1)
        data = {'title': 'booking1', 'booked_from': time_from,
                'booked_to': time_to, 'room_booked': '/rooms/1/'}
        response = self.client.post('/bookings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # user can't do booking during the staff meeting (created in setup)
        time_from = timezone.now() + timedelta(hours=1)
        time_to = time_from + timedelta(hours=1)
        data = {'title': 'booking1', 'booked_from': time_from,
                'booked_to': time_to, 'room_booked': '/rooms/1/'}
        response = self.client.post('/bookings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admins(self):
        '''Check if "is_staff" users can delete other users rooms,
            meetings and other users'''
        # first we'll create a new room and meeting as a user
        client = APIClient()
        username = 'testuser'
        password = 'pass123Word'
        self.client.login(username=username, password=password)
        time_from = timezone.now()
        time_to = time_from + timedelta(minutes=59)
        data = {'title': 'booking1', 'booked_from': time_from,
                'booked_to': time_to, 'room_booked': '/rooms/1/'}
        response = self.client.post('/bookings/', data, format='json')
        data = {'name': 'room_name1', 'location': 'somehwere1'}
        response = self.client.post('/rooms/', data, format='json')
        client.logout()
        # login as 'is_staff' user and del room and booking of different user
        username = 'teststaffuser'
        self.client.login(username=username, password=password)
        response = self.client.delete('/bookings/2/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete('/rooms/2/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
