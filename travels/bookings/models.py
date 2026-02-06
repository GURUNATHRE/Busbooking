from django.db import models
from django.contrib.auth.models import User

# Users Model
# class Users(models.Model):
#     first_name = models.CharField(max_length=20)
#     last_name = models.CharField(max_length=10)
#     email_id = models.EmailField(max_length=25)
#     mobile_no = models.CharField(max_length=10)
    
#     def __str__(self):
#         return f"{self.first_name}, {self.last_name}"


# Buses Model
class Buses(models.Model):
    bus_name = models.CharField(max_length=30)  
    bus_number = models.CharField(max_length=20, default='0')  
    starting_point = models.CharField(max_length=40)
    ending_points = models.CharField(max_length=30)
    features = models.TextField(max_length=100)
    total_seats = models.BigIntegerField()
    start_time = models.TimeField()
    reach_time = models.TimeField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=1)
    
    def __str__(self):
        return self.bus_name  

    
# Seats Model
class Seats(models.Model):
    bus = models.ForeignKey(Buses, on_delete=models.CASCADE, related_name="buses_seat")
    seat_no = models.CharField(max_length=10)
    seat_book = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('bus', 'seat_no')
    
    def __str__(self):
        return f"{self.bus.bus_name} - {self.seat_no}"
#Bookings Model:
class Bookings(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bokkings_by_user")
    bus = models.ForeignKey(Buses , on_delete=models.CASCADE ,related_name="booking_do_in_which_bus")
    seat = models.ForeignKey(Seats,on_delete=models.CASCADE,related_name="user_seat")
    booking = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"User: {self.user.first_name} {self.user.last_name}, Bus: {self.bus.bus_name}, Seat: {self.seat.seat_no}, Amount: {self.bus.price}, Booking Time: {self.booking}"