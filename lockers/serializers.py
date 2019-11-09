from rest_framework import serializers

from .models import *


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class NumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['number']


