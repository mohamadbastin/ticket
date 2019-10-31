from django.shortcuts import render
from rest_framework import status, authentication
from rest_framework.permissions import IsAuthenticated, AllowAny
import requests
from rest_framework.views import APIView

from .serializers import *
# Create your views here.
from .models import *
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, UpdateAPIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework.authtoken.views import ObtainAuthToken

make = PaymentLinks.objects.get(name='make').link
pay = PaymentLinks.objects.get(name='pay').link
check = PaymentLinks.objects.get(name='check').link
api_key = Terminal.objects.get(name='poolam').api_key
poolam = Terminal.objects.get(name='poolam')


class ProfileListView(ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usr = self.request.user
        user = Profile.objects.filter(user=usr)
        return user


class HallListView(ListAPIView):
    serializer_class = HallSerializer
    permission_classes = [IsAuthenticated]
    queryset = Hall.objects.all()


class CheckBought(GenericAPIView):
    def post(self, request):
        id = self.request.data.get('id', None)

        if id:
            try:
                usr = User.objects.get(username=id)
            except:
                return Response('user does not exist')
            user = Profile.objects.get(user=usr)
            t = Ticket.objects.filter(profile=user)
            if t:
                return Response(False)

        return Response(True)

    # return Response({})


class SeatReserveView(CreateAPIView):
    serializer_class = SeatSerializer

    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        #         [{seat_pk:usr},{pk_seat:usr}]

        a = self.request.data
        for i in a:
            for j in i:
                pass
        # TODO reserve tickets
        return Response({})


class BuyTicketView(CreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        Hall.objects.all()
        # TODO
        pass


class SetInvoice(CreateAPIView):
    # permission_classes = [IsAuthenticated, ]
    serializer_class = InvoiceSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        amount = data.get('amount')
        make_response = requests.post(make, data={"api_key": api_key, "amount": amount,
                                                  "return_url": "http%3A%2F%2Fapi.moarefe98.ir%2Fadmin%2F"})
        status = (make_response.json()["status"])

        if status == 1:
            invoice_key = (make_response.json()["invoice_key"])
            Invoice.objects.create(terminal=poolam, amount=amount, key=invoice_key, status='w', )
            pay_link = str(pay) + str(invoice_key)
            # print (pay)
            # print(pay_link)
            return HttpResponseRedirect(pay_link)
        else:
            # TODO CANCEL

            pass

        return Response('done')


class CheckPayView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        # TODO CHECK PAYMENT AND REDIRECT
        pass


class SignupView(CreateAPIView):
    serializer_class = ProfileSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        student_id = data.get('student_id', None)
        national_id = data.get('national_id', None)
        name = data.get('name', None)
        picture = data.get('picture', None)
        gender = data.get('gender', None)
        major = data.get('major', None)
        major = Major.objects.get(pk=major)
        phone = data.get('phone', None)

        try:
            temp_user = User.objects.create(username=student_id, password=national_id)
        except:
            msg = 'این کاربر قبلا ثبت نام شده!'
            return Response(msg, status=status.HTTP_409_CONFLICT)

        temp_profile = Profile.objects.create(name=name, phone=phone, major=major, gender=gender, picture=picture,
                                              student_id=student_id, national_id=national_id, user=temp_user)

        return Response(True, status=status.HTTP_200_OK)


class MajorListView(ListAPIView):
    serializer_class = MajorSerializer
    queryset = Major.objects.all()


class MajorCreateView(CreateAPIView):
    serializer_class = MajorSerializer

    def post(self, request, *args, **kwargs):
        name = request.data.get('name')

        temp_major = Major.objects.create(name=name)

        return temp_major


# TODO GET BLOCKS
class BlockListView(ListAPIView):
    serializer_class = BlockSerializer
    permission_classes = [IsAuthenticated]
    queryset = Block.objects.all()


# TODO RESERVE SEATS
# TODO ASSIGN SEATS AND CREATE TICKETS


# TODO SHOW TICKETS
class TicketListView:
    pass  # TODO HOW TO RETRIEVE TICKETS BOUGHT BY USER NOT ONLY OWNED BY USER

# TODO CREATE BLACKLIST
