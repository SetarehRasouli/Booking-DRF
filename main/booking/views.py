from django.db import IntegrityError, transaction
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Provider, Booking
from datetime import datetime
from .serializers import AvailableSlotsSerializer, BookingSerializer, ProviderSerializer
from rest_framework import viewsets, permissions
# Create your views here.

class AvialableSlotsView(APIView):
    def get(self, request, provider_id):
        provider=Provider.objects.get(id=provider_id)

        date_str=request.query_params.get('date')
        # date=datetime.strptime(date_str, '%Y-%m-%d').date()
        
        if not date_str:
            return Response(
                {'error':'The date is needed.'},
                status=400
            )
        try: 
            date=datetime.strptime(date_str, '%Y-%m-%d').date()

        except ValueError:
            return Response(
                {'error':'Invalid format.'},
                status=400
            )

        slots=provider.get_available_slots(date)
        serializer = AvailableSlotsSerializer(slots, many=True)
        return Response(serializer.data)



class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError("This slot is already booked. Please choose another time.")