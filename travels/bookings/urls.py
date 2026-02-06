from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns
from .views import Registerview,Loginview,Bookingview,Userview,BusView,SingleBus,SeatView
urlpatterns = [
    # path('users/',usersview),
    # path('users/<int:pk>',userfulldetailview),
    path('Loginview/',Loginview.as_view()), 
    path('register/',Registerview.as_view()),
    path('buses/',BusView.as_view()),
    path('buses/<int:pk>',SingleBus.as_view()),
    path('seats/',SeatView.as_view()),
    path('Bookingview/',Bookingview.as_view()),
    path('Userview/<int:user_id>',Userview.as_view())
]
#formatsufiixes this is usseful to get data basd
# urlpatterns = format_suffix_patterns(urlpatterns)
 