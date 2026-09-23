from django.contrib import admin
from .models import Provider, Booking, BlockedTime

# Register your models here.
admin.site.register(Provider)
admin.site.register(Booking)
admin.site.register(BlockedTime)