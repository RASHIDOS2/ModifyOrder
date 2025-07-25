
from rest_framework import serializers

from .models import Orders, ModifyDoors


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class ModifyOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModifyDoors
        fields = '__all__'

