# Create your views here.

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect


# Create your views here.
from .serializers import *


class CartViewList(ListAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()


class NumberView(CreateAPIView):
    serializer_class = NumberSerializer

    def post(self, request, *args, **kwargs):
        a = self.request.data.get('number')
        try:
            b = Cart.objects.get(number=a)
        except:
            return Response('کارتی با این مشحصات وجود ندارد! دوباره امتحان کنید.')
        msg = ' نام صاحب کارت: ' + str(b.owner)

        return Response(msg)


class ListRedirectView(CreateAPIView):
    serializer_class = NumberSerializer

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect('http://ticket.moarefe98.ir/media/lockers.pdf')