from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Orders, ModifyDoors

from .serializers import OrderSerializer, ModifyOrderSerializer


class OrdersAPIView(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    lookup_field = 'uuid'
    serializer_class = OrderSerializer


class ModifyOrdersAPIView(viewsets.ModelViewSet):
    queryset = ModifyDoors.objects.all()
    lookup_field = 'uuid'
    serializer_class = ModifyOrderSerializer
