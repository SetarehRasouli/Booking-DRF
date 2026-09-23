from datetime import datetime, timedelta, time
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Provider(models.Model):
    name = models.CharField(max_length=150)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=200)
    start_time=models.TimeField()
    end_time=models.TimeField()

    def get_available_slots(self, date, slot_duration_minutes=30):
        start_datetime = timezone.make_aware(datetime.combine(date, self.start_time))
        end_datetime = timezone.make_aware(datetime.combine(date, self.end_time))

        bookings = Booking.objects.filter(
            provider = self,
            time__date=date,
            status='booked'
        )

        booked_times = [b.time for b in bookings]
        # booked_times = []
        # for b in bookings:
        #     booked_times.append(b.time)

        blocked = BlockedTime.objects.filter(provider=self, start_time__date=date)

        slots=[]
        current=start_datetime
        while current < end_datetime:
            slot_end = current + timedelta(minutes=slot_duration_minutes)

            is_booked = current in booked_times
            is_blocked = any(b.start_time <= current < b.end_time for b in blocked)

            if not is_booked and not is_blocked:
                slots.append({'start_time': current, 'end_time': slot_end})

            current = slot_end
        return slots


class Booking(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    time = models.DateTimeField()
    duration = models.DurationField(blank=True, null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')
    class Meta:
        unique_together = ('provider', 'time')


class BlockedTime(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    reason = models.TextField( blank=True, null=True)
