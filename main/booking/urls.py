from rest_framework.routers import DefaultRouter
from .views import AvialableSlotsView, BookingViewSet
from django.urls import path, include


router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='bookings')

urlpatterns = [
    path('', include(router.urls)),
    path('providers/<int:provider_id>/available-slots/', AvialableSlotsView.as_view(), name='available-slots'),
]
