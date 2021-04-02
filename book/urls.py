from django.urls import path, include
from book import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('user_auth', views.UserViewSet, basename='user')
router.register('rooms', views.Meeting_roomView)
router.register('bookings', views.BookingView, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
