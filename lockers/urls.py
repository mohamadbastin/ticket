# from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('card/', NumberView.as_view()),
    path('list/', ListRedirectView.as_view())

]
