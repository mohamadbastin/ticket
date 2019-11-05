import requests
from django.http import HttpResponseRedirect
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Create your views here.
from rest_framework.views import APIView

from .serializers import *

make = PaymentLinks.objects.get(name='make').link
pay = PaymentLinks.objects.get(name='pay').link
check = PaymentLinks.objects.get(name='check').link
api_key = Terminal.objects.get(name='poolam').api_key
poolam = Terminal.objects.get(name='poolam')
token = poolam.token

gap_time = 10

sn98 = [9830317, 9830339, 9830340, 9830341, 9830342, 9830343, 9830344, 9830345, 9830346, 9830354, 9830383, 9830384,
        9830385, 9830386, 9830387, 9831866, 9832061, 9832062, 9832063, 9832064, 9832065, 9832066, 9832067, 9832068,
        9832069, 9832070, 9832071, 9832072, 9832073, 9832074, 9832075, 9832076, 9832077, 9832078, 9832079, 9832080,
        9832081, 9832082, 9832083, 9832084, 9832085, 9832086, 9832087, 9832088, 9832089, 9832090, 9832091, 9832092,
        9832093, 9832094, 9832095, 9832096, 9832097, 9832098, 9832099, 9832100, 9832101, 9832102, 9832103, 9832104,
        9832105, 9832106, 9832107, 9832108, 9832109, 9832110, 9832111, 9832112, 9832113, 9832114, 9832342, 9832343,
        9832344, 9832345, 9832346, 9832347, 9832348, 9832349, 9832350, 9832351, 9832352, 9832353, 9832354, 9832355,
        9832356, 9832357, 9832358, 9832359, 9832360, 9832361, 9832362, 9832363, 9832364, 9832365, 9832366, 9832367,
        9832368, 9832369, 9832370, 9832371, 9832372, 9832373, 9832374, 9832375, 9832376, 9832377, 9832378, 9832379,
        9832380, 9832381, 9832382, 9832383, 9832384, 9832385, 9832386, 9832387, 9832388, 9832389, 9832390, 9832391,
        9832392, 9832393, 9832394, 9832395, 9832396, 9832397, 9832398, 9832399, 9832400, 9832401, 9832402, 9832403,
        9832404, 9833520, 9833521, 9833527, 9833540, 9833548, 9833563, 9833566, 9833567, 9833572, 9833575, 9833583,
        9833584, 9833587, 9833590, 9833591, 9833602, 9833615, 9833644]


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

    def get_queryset(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)

        res = Reservation.objects.all()
        for i in res:
            if not i.is_deleted:
                if timezone.now() - i.res_date_time >= timezone.timedelta(minutes=gap_time):
                    print("heree")
                    i.is_deleted = True
                    s = i.seat
                    s.status = 'A'
                    s.save()
                    i.save()
        for i in res:
            if i.is_deleted:
                s = i.seat
                s.status = 'A'
                s.save()
        for i in res:
            if not i.is_deleted and i.profile == profile:
                s = i.seat
                s.status = 'M'
                s.save()

        return Hall.objects.all()


class CheckBought(ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        usr = self.request.user
        user = Profile.objects.get(user=usr)
        t = Ticket.objects.filter(profile=user)
        if t:
            return Response(False)

        return Response(True)

    # return Response({})


def get_amount(profile):
    a = profile.student_id
    # print(int(a) in sn98)
    if int(a) in sn98:
        return 'free'
    return Price.objects.get(name='azad').price


def set_invoice(profile):
    amount = get_amount(profile)
    if amount == 'free':
        amount = 0
        a = Invoice.objects.create(terminal=poolam, amount=amount, key='free', status='w')
        return a

    else:
        # token
        url = "http%3A%2F%2Fmoarefe98.ir%2Fticket%2Fpayment%2Fgateway%2Fcallback%2F%3Ftoken%3D" + token
        make_response = requests.post(make, data={"api_key": api_key, "amount": amount,
                                                  "return_url": url})
        status = (make_response.json()["status"])
        # print(1)
        print(status)
        if status == 1:
            invoice_key = (make_response.json()["invoice_key"])
            a = Invoice.objects.create(terminal=poolam, amount=amount, key=invoice_key, status='w', )
            return a


class SeatReserveView(CreateAPIView):
    serializer_class = SeatSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # {'pk': 2}
        a = self.request.data.get('pk', None)
        try:
            user = self.request.user
            profile = Profile.objects.get(user=user)
        except:
            return Response({'msg': 'user not valid'}, status=status.HTTP_401_UNAUTHORIZED)
        if a:
            seat = Seat.objects.get(pk=a)
            if seat.status == 'A' or seat.status == 'M':
                res = Reservation.objects.create(seat=seat, profile=profile, )
                invoice = set_invoice(profile)
                print(invoice)
                invoice.reservation = res
                invoice.save()
                seat.status = 'S'
                seat.save()
                msg = {'msg': 'صندلی شما رزور شد.', 'amount': invoice.amount, 'pk': invoice.pk,
                       'profile': {'name': profile.name},
                       'seat': {'block': seat.row.block.name, 'row': seat.row.number, 'seat': seat.number}}
                return Response(msg, status=status.HTTP_200_OK)
        msg = {'msg': 'این صندلی قبلا فروخته شده. لطفا صفحه را رفرش کنید.'}
        return Response(msg, status=status.HTTP_401_UNAUTHORIZED)


class ReservationListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        res = Reservation.objects.get(profile=profile)
        seat = res.seat
        invoice = res.invoice.first()
        print(res)
        print(ReservationSerializer(instance=res).data)
        print(invoice)
        print(invoice.key)
        msg = {'msg': 'صندلی شما رزور شد.', 'amount': invoice.amount, 'pk': invoice.pk,
               'profile': {'name': profile.name, 'student_id': profile.student_id, 'phone': profile.phone},
               'seat': {'block': seat.row.block.name, 'row': seat.row.number, 'seat': seat.number}}
        return Response(msg, status=status.HTTP_200_OK)


class BuyTicketView(CreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        pk = request.data.get('pk', None)
        if pk:
            # invoice = Invoice.objects.get(pk=pk)
            res = Reservation.objects.get(profile=profile)
            if res.is_deleted:
                return HttpResponseRedirect('http://moarefe98.ir/ticket/')
            invoice = Invoice.objects.get(reservation=res)
            if invoice.key == 'free':
                a = Ticket.objects.create(seat=invoice.reservation.seat, profile=invoice.reservation.profile)
                s = invoice.reservation.seat
                s.status = 'S'
                s.save()
                invoice.status = 't'
                invoice.ticket = a
                invoice.save()
                b = invoice.reservation
                b.ticket = a
                b.is_deleted = True
                b.save()

                # ss = SeatSerializer(instance=s).data
                pp = ProfileSerializer(instance=profile).data

                # return HttpResponseRedirect('http://moarefe98.ir/ticket/ticket-pdf.html')
                return HttpResponseRedirect('http://google.com/')
                # return Response({'ticket': {'id': a.pk, 'date': a.date,
                #                             'seat': {'number': s.number, 'row': s.row.number,
                #                                      'block': s.row.block.name}, 'profile': pp}})

            else:
                amount = invoice.amount
                key = invoice.key



        msg = {'msg': 'مشکلی پیش آمده'}
        return Response(msg, status=status.HTTP_404_NOT_FOUND)


class BuyTicket2View(CreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def post(self, request, *args, **kwargs):
        tk = self.request.data.get('token', None)
        in_key = self.request.data.get('id', None)
        if tk == token:
            try:
                invoice = Invoice.objects.get(key=in_key)
            except:
                return HttpResponseRedirect('http://google.com/')
            status = request.data.get('status')
            if status == 1:
                a = Ticket.objects.create(seat=invoice.reservation.seat, profile=invoice.reservation.profile)
                s = invoice.reservation.seat
                s.status = 'S'
                s.save()
                invoice.status = 't'
                invoice.ticket = a
                invoice.save()
                b = invoice.reservation
                b.ticket = a
                b.is_deleted = True
                b.save()



            else:
                HttpResponseRedirect('http://google.com/')
        else:
            return HttpResponseRedirect('http://google.com/')


# class CheckPayView(CreateAPIView):
#     def post(self, request, *args, **kwargs):
#         #
#         pass


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


class BlockListView(ListAPIView):
    serializer_class = BlockSerializer
    permission_classes = [IsAuthenticated]
    queryset = Block.objects.all()


# TODO ASSIGN SEATS AND CREATE TICKETS


# TODO SHOW TICKETS
class TicketListView(ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        profile = Profile.objects.get(user=user)

        a = Ticket.objects.get(profile=profile)
        s = a.seat
        pp = ProfileSerializer(instance=profile).data

        return Response({'ticket': {'id': a.pk, 'date': a.date,
                                    'seat': {'number': s.number, 'row': s.row.number,
                                             'block': s.row.block.name}, 'profile': pp}})


# TODO CREATE BLACKLIST


class TestView(APIView):
    serializer_class = MajorSerializer

    def post(self, request, *args, **kwargs):
        # tk = self.request.GET.get('token')

        return HttpResponseRedirect('http://moarefe98.ir/ticket/ticket-pdf.html')
