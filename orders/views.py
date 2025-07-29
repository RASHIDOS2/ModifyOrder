from django.shortcuts import render
from rest_framework import generics, permissions, viewsets, status
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


class CheckOrderView(APIView):
    def get(self, request):
        title = request.query_params.get('title', '')

        try:
            # Ищем заказ по точному совпадению title
            order = Orders.objects.get(title__iexact=title)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Orders.DoesNotExist:
            return Response(
                {'error': 'Заказ не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

class GetModifyView(APIView):
    def get(self, request):
        modify_order = request.query_params.get('order_id', '')

        try:
            modify_order = ModifyDoors.objects.get(order_id__exact=modify_order)
            serializer = ModifyOrderSerializer(modify_order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ModifyDoors.DoesNotExist:
            return Response(
            {'error': 'Заказ не найден'},
            status=status.HTTP_404_NOT_FOUND
        )
