from django.contrib import admin
from .models import Buses,Seats,Bookings
# Register your models here.
# admin.py
from django.contrib.auth.admin import UserAdmin



admin.site.register(Buses)
admin.site.register(Seats)
admin.site.register(Bookings)