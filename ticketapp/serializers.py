from rest_framework import serializers

from .models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user']


class SeatSerializer(serializers.ModelSerializer):
    # owner = ProfileSerializer(many=True)

    class Meta:
        model = Seat
        fields = ['pk', 'number', 'title', 'price', 'description', 'ad', 'status']


class RowSerializer(serializers.ModelSerializer):
    seat = SeatSerializer(many=True)

    class Meta:
        model = Row
        fields = ['pk', 'number', 'seat']


class BlockSerializer(serializers.ModelSerializer):
    row = RowSerializer(many=True)

    class Meta:
        model = Block
        fields = ['pk', 'name', 'gender', 'row']


class HallSerializer(serializers.ModelSerializer):
    block = BlockSerializer(many=True)

    class Meta:
        model = Hall
        # read_only_fields = ['name', 'block']
        fields = ['name', 'block']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    seat = SeatSerializer(many=True)
    profile = ProfileSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['date', 'profile', 'seat']


class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ['pk', 'name']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
