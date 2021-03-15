from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from book.models import Meeting_room, Booking
from book.serializer import UserSerializer, UserAdminSerializer
from book.serializer import Meeting_roomSerializer, BookingSerializer
from rest_framework.exceptions import NotFound
from book.permissions import IsOwnerOrStaffOrReadOnly, IsStaffOrReadPutOnly


class UserViewSet(viewsets.ModelViewSet):
    """
    Endpoint that allows users to be creted, viewed, edited, deleted.
    """
    permission_classes = [permissions.IsAuthenticated, IsStaffOrReadPutOnly]
    
    #the 'is_staff' user can access additional fields so the viewset gets 
    #serializer based on users 
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return UserAdminSerializer
        return UserSerializer

    #a specific queryset for the User view, user can see himself only
    #or if user 'is_staff', all records available
    def get_queryset(self):
        if self.request.user.is_staff :
            queryset = User.objects.all()
        else:
            queryset = User.objects.filter(username=self.request.user)
        return queryset

class Meeting_roomView(viewsets.ModelViewSet):
    """
    Endpoint that allows meeting rooms to be creted, viewed or deleted.
    """
    queryset = Meeting_room.objects.all()
    serializer_class = Meeting_roomSerializer
    permission_classes = [permissions.IsAuthenticated, 
                          IsOwnerOrStaffOrReadOnly]

    #adds the owner of record based on user    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BookingView(viewsets.ModelViewSet):
    """
    Endpoint that allows meetings to be created, viewed or deleted.
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrStaffOrReadOnly]

    def get_queryset(self):
        """
        Optionally restricts the queryset if the query parameters are set
        in the url in the form of:
        'bookings?first_name=FirstName&last_name=LastName' 
        """
        queryset = Booking.objects.all()
        #bookings?first_name=Name&last_name=Last_Name
        first_name = self.request.query_params.get('first_name', None)
        last_name = self.request.query_params.get('last_name', None)
        user = User.objects.filter(first_name=first_name, last_name=last_name)
        if user.exists():
            queryset = queryset.filter(owner=user[0].id)
        elif first_name is not None and last_name is not None:
            raise NotFound('The users name searched does not exist')
        return queryset

    #adds the owner of record based on user 
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)