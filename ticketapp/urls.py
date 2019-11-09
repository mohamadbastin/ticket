# from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('profile/', ProfileListView.as_view()),
    path('hall/', HallListView.as_view()),
    path('buy/', BuyTicketView.as_view()),
    path('check/', CheckBought.as_view()),
    path('reserve/', SeatReserveView.as_view()),
    path('majors/', MajorListView.as_view()),
    path('signup/', SignupView.as_view()),
    path('reservation/', ReservationListView.as_view()),
    path('ticket/', TicketListView.as_view()),
    path('test/', TestView.as_view()),
    path('payment/gateway/callback/', BuyTicket2View.as_view()),
    path('qr/enter/', EnterServiceView.as_view()),
    path('qr/food/', FoodServiceView.as_view()),
    path('qr/pixel/', PixelServiceView.as_view()),
    path('serv/', ServiceView.as_view())

]
