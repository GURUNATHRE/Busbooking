from rest_framework.decorators import api_view       
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.http import Http404
from .serializers import BusSerializer,Seatsinfoserializer,UserResgister_serilizer,Bookingserializer
from .models import  Buses,Seats,Bookings,User
#no decoratos it is ws
from rest_framework.views import APIView   
from rest_framework import status,generics    
#authentication 
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authtoken.models import Token



import pdb

# @api_view(['GET','POST'])
# def usersview(request):
#     if request.method == 'GET':
#         users = Users.objects.all()
#         serializers =UserSerializer(users,many=True)
#         return Response(serializers.data, status=status.HTTP_200_OK)
#     elif request.method =='POST':
#         serializers = UserSerializer(data = request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data,status=status.HTTP_201_CREATED)
#         return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

# #particular student data
# @api_view(['GET','PUT','DELETE'])
# def userfulldetailview(request,pk):
#     try:
#         # pdb.set_trace()
#         if request.method == 'GET':
#             singleuser = Users.objects.get(pk=pk)
#             serializer = UserSerializer(singleuser)
#             return  Response(serializer.data, status=status.HTTP_200_OK)
#         elif request.method == 'PUT':
#             singleuser = Users.objects.get(pk=pk)
#             serializer = UserSerializer(singleuser,data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
#             else:
#                 return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#         elif request.method == 'DELETE':
#             singleuser = Users.objects.get(id=pk)
#             singleuser.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
        
#     except Users.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)


#Auth
class Registerview(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserResgister_serilizer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
class Loginview(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        username = request.data.get('username')
        password = request.data.password('password')
        user = User.objects.get(username=username,password=password)
        if user:
            token,created = Token.objects.get_or_create(user=user)
            return Response({"token  " :token.key},status=status.HTTP_200_OK)
        return Response({"error": "invalid"},status=status.HTTP_401_UNAUTHORIZED)


#class based view 
class BusView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        buses = Buses.objects.all()
        serializer = BusSerializer(buses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = BusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #to retrive the single object
    
class Bookingview(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    def post(self, request):
        seat_id = request.data.get('seat')

        try:
            seat = Seats.objects.get(id=seat_id)

            if seat.seat_book:
                return Response({"error": "Seat is already booked"}, status=status.HTTP_400_BAD_REQUEST)

            seat.seat_book = True
            seat.save()

            booking = Bookings.objects.create(
                user=request.user,
                bus=seat.bus,
                seat=seat.seat_no
            )

            serializer = Bookingserializer(booking)

            return Response({"message": "Seat is booked", "booking": serializer.data}, status=status.HTTP_202_ACCEPTED)

        except Seats.DoesNotExist:
            return Response({"error": "Seat not found"}, status=status.HTTP_400_BAD_REQUEST)
    # def post(self,request):
    #     seat_id = request.data.get('seat')
    #     try :
    #         seat = Seats.objects.get(seat_id = Seats.seat_no)
    #         if seat.seat_book:
    #             return Response({"error": "seat is already booked"},status=status.HTTP_400_BAD_REQUEST)
    #         seat.seat_book = True
    #         seat.save()
    #         bookings = Bookings.objects.create(
    #             user = request.User,
    #             bus = Seats.Buses,
    #             seat = Seats.seat_no
    #         )
    #         serializer = Bookingserializer(bookings)

    #         return Response(serializer.data,{"mesage" : "seat is booked"},status=status.HTTP_202_ACCEPTED)
    #     except seat.DoesNotExist:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
            

class Booking_details_view(APIView):
    permission_classes = [AllowAny]
    def get(self,request,user_id):
        if request.user_id != user_id:
            return Response({"error": "user_id doen't Exist"})
        object = Bookings.objects.filter(user_id=user_id)
        serializers = Bookingserializer(object)
        return Response(serializers.data, status=status.HTTP_200_OK)

class Userview(APIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
            bookings = Bookings.objects.filter(user_id=user_id)

            if not bookings.exists():
                return Response({"detail": "No bookings found for this user."}, status=status.HTTP_404_NOT_FOUND)

            serializer = Bookingserializer(bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    

#class based view getting single obj based on pk
class SingleBus(APIView):
    def get_object(self,pk):
        try:
            return Buses.objects.get(pk=pk)
        except Buses.DoesNotExist:
            raise Http404
    def get(self,request,pk):
        bus = self.get_object(pk)
        serilizer = BusSerializer(bus)
        return Response(serilizer.data,status=status.HTTP_200_OK)
    def post(self,request,pk):
        serilizer = BusSerializer(data=request.data)
        return Response(serilizer.data,status=status.HTTP_201_CREATED)
    def put(self,request,pk):
        bus = self.get_object(pk)
        serilizer = BusSerializer(bus,data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serilizer.data,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        bus = self.get_object(pk)
        bus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#pagination

class SeatsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
#class basd view for seats 
class SeatView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        seats = Seats.objects.all()
        paginator = SeatsPagination()
        result_page = paginator.paginate_queryset(seats, request)
        serializer = Seatsinfoserializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


