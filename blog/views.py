from django.shortcuts import render
from .serializers import *
# Create your views here.
from .models import *
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, UpdateAPIView
from rest_framework.response import Response


class PostView(ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class SponsorView(ListAPIView):
    serializer_class = SponsorSerializer
    queryset = Sponsor.objects.all()


class SinglePostView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        pid = self.kwargs.get('pid', None)
        if pid:
            return Post.objects.filter(pk=pid)


class SingleSponsorView(ListAPIView):
    serializer_class = SponsorSerializer

    def get_queryset(self):
        sid = self.kwargs.get('sid', None)
        if sid:
            return Sponsor.objects.filter(pk=sid)

