from django.db.models import Prefetch
from django.shortcuts import render
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from services.models import Service
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


class ModifyDoorsWRListView(APIView):
    def get(self, request, *args, **kwargs):
        # 1. Получаем все объекты ModifyDoors со статусом WR
        modify_doors = ModifyDoors.objects.filter(
            site_status='WR'
        ).select_related('order_id').prefetch_related(
            Prefetch(
                'service_set',
                queryset=Service.objects.all(),
                to_attr='services'
            )
        )

        # 2. Формируем структуру ответа
        result = []
        for modify in modify_doors:
            # 3. Создаем список услуг для текущей модификации
            services_list = []
            for service in modify.services:
                services_list.append({
                    'service_id': service.uuid,
                    'size': service.size,
                    'angleCut': service.angleCut,
                    'hinges': service.hinges,
                    'latchLeader': service.latchLeader,
                    'holeLock': service.hole_lock,  # Преобразуем hole_lock → holeLock
                    'opening': service.open_type  # Преобразуем open_type → opening
                })

            # 4. Добавляем элемент в результирующий список
            result.append({
                'order_id': str(modify.order_id.uuid),  # UUID связанного заказа
                'modification': {
                    'modify_id': str(modify.uuid),
                    'services': services_list
                }
            })

        return Response(result, status=status.HTTP_200_OK)