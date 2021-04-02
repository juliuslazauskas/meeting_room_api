## Meeting booking api

API has these views:
* API-root view which is read-only accesible to everytone (can be changed to `IsAuthenticated` users by changing the Django project `settings.py` :
`REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ]
}`

* User view (`user_auth`) which allows to create, view, modify or delete users.  
* Meeting room view (`rooms`) which allows to create, view or delete rooms.
* Booking view (`bokings`) which allows to create, view or delete bookings. Booking view also has a filter by users in the url:
    `/bookings?first_name=Name&last_name=Last_Name`
* Login view (`/api-auth/login/`) for a login if using browser
* Logout view (`/api-auth/logout`)

At least one superuser must be created using `python manage.py createsuperuser` This user can then login into API and create other users. Users are 2 levels: 
1. Users that have 'is_staff' flag and they can create/modify/delete other users, rooms or bookings
    `GET /user_auth/`
    `POST, PUT /user_auth/ {'username': 'unique_username', 'email':'mail@mail.com', 'first_name':'First_name', 'last_name':'Last_Name', 'password':'some_password', 'is_staff':True/False}` 
    `DELETE /user_auth/id/`
2. Users that dont have 'is_staff' flag, they can view only themselves in the user view and change their password:

    `GET /user_auth/`
    `PUT /user_auth/ {'username': 'unique_username', 'email':'mail@mail.com', 'first_name':'First_name', 'last_name':'Last_Name', 'password':'some_password'}`

password is a `write_only` field in the views, users can't see it and passwords are hashed using `django.contrib.auth.hashers` and password hashes are stored in DB

All users can create meeting rooms and bookings, but only owners (users that created them) or users with 'is_staff' flag can delete entries. Meeting rooms and Bookings get an extra field 'owner' for the user that created particular record. To access all views, except root view, and /api-auth/login or /api-auth/logout user must be authenticated and include username and password in the requests. 
    `GET /rooms/`
    `POST /rooms/ {'name': 'Meting_room_name', 'location':'Meeting_room_location'}`
    `DELETE /rooms/id/`
    `GET /bookings/`
    `POST /bookings/ {'title': 'Meeting_title', 'booked_from':'YYYY-mm-ddThh:mm', 'booked_to':'YYYY-mm-ddThh:mm', 'room_booked':'/rooms/id/'}` 
    `DELETE /bookings/id/`
All views, except api-root, are protected by `IsAuthenticated`. User view has additional `permissions` set up so that 'is_staff' user can access other users, but other user can see or edit only himself. 

Meeting room fields must be unique together.

Booking view validates entries so no double booking can occur in the same room.



