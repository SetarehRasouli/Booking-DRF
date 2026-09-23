from rest_framework import serializers
from .models import Provider, Booking, BlockedTime

class ProviderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model= Provider
        fields = [
            'id',
            'name',
            'user',
            'email',
            'start_time',
            'end_time',
        ]


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Booking
        fields = [
            'id',
            'provider',
            'time',
            'duration',
            'user',
            'created_at',
            'status',
        ]

    def validate(self, data):
        provider=data['provider']
        requested_time=data['time']
        
        available_slots = provider.get_available_slots(requested_time.date())
        available_times=[slot['start_time'] for slot in available_slots]

        if requested_time not in available_times:
            raise serializers.ValidationError(
                "You cann't reserve this time(reserved or out of the provider work time)."
            )

        return data



class AvailableSlotsSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
