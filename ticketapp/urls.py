# from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', ProfileListView.as_view()),
    path('hall/', HallListView.as_view()),
    path('res/', SeatReserveView.as_view()),
    path('check/', CheckBought.as_view()),
    path('red/', SetInvoice.as_view()),
    path('majors/', MajorListView.as_view())

]

