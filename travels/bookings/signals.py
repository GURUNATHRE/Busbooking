from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Seats, Buses

@receiver(post_save, sender=Buses)
def update_available_seats(sender, instance, created, **kwargs):
    if created:
        for i in range(1, instance.total_seats + 1):
            Seats.objects.create(bus=instance, seat_no=f'Seat no: {i}')
