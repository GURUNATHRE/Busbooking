from rest_framework import serializers
from bookings.models import  Buses,Seats,Bookings

# for authentiation using auth 
from django.contrib.auth.models import User

#regisration for user from serilisers 

class UserResgister_serilizer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True)
    class Meta:
        model  = User
        fields = ['username','email','password']
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user
# Serializer for Users model
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Users
#         fields = "__all__"

# Serializer for Buses model
class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buses
        fields = "__all__"
#serializer for seats 
class Seatsinfoserializer(serializers.ModelSerializer):
    class Meta:
        model = Seats
        fields = ['bus','seat_no','seat_book']

class Bookingserializer(serializers.ModelSerializer):
    bus = serializers.StringRelatedField(read_only=True)
    seat = Seatsinfoserializer(read_only=True) 
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Bookings
        fields = "__all__"
