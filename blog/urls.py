# from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('posts/', PostView.as_view()),
    path('sponsors/', SponsorView.as_view()),
    path('sponsors/<sid>', SingleSponsorView.as_view()),
    path('posts/<pid>', SinglePostView.as_view())
]

