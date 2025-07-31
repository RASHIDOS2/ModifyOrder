from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import ModifyDoors
from services.models import Service, Characteristics
from services.serializers import ServiceSerializer, CharacteristicsSerializer


# Create your views here.
class ServicesAPIView(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'uuid'


class CharacteristicsAPIView(viewsets.ModelViewSet):
    queryset = Characteristics.objects.all()
    serializer_class = CharacteristicsSerializer
    lookup_field = 'uuid'

class GetServicesAPIView(viewsets.ViewSet):
    def list(self, request):
        id_modify = request.query_params.get('id_modify', '')

        try:
            services = Service.objects.filter(id_modify=id_modify)
            serializer = ServiceSerializer(services, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Service.DoesNotExist:
            return Response(
            {'error': 'Заказ не найден'},
            status=status.HTTP_404_NOT_FOUND
        )


class GetCharacteristicsAPIView(viewsets.ViewSet):
    def list(self, request):
        id_service = request.query_params.get('id_service', '')

        try:
            orders = Characteristics.objects.filter(id_service=id_service)
            serializer = CharacteristicsSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Characteristics.DoesNotExist:
            return Response(
                {'errror': 'Закзаз не найден'},
                status=status.HTTP_404_NOT_FOUND
            )


class ServicesUpdate(APIView):
    def put(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            return Response(
                {"error": "Expected a list of items"},
                status=status.HTTP_400_BAD_REQUEST
            )
        updated_items = []
        errors = []
        modify_door_id = None
        with transaction.atomic():
            for service_data in request.data:
                if 'id' not in service_data:
                    errors.append({"error": "Missing ID for item"})
                    continue

                try:
                    instance = Service.objects.get(id=service_data['id'])
                except Service.DoesNotExist:
                    errors.append({"error": f"Item not found: {service_data['id']}"})
                    continue

                # Если это первая услуга - запоминаем связанный ModifyDoors
                if modify_door_id is None:
                    modify_door_id = instance.id_modify_id

                serializer = ServiceSerializer(instance, data=service_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    updated_items.append(serializer.data)
                else:
                    errors.append({
                        "id": service_data['id'],
                        "errors": serializer.errors
                    })

            # Если есть ошибки - откатываем транзакцию
            if errors:
                transaction.set_rollback(True)
                return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

            # Обновляем статус ModifyDoors
            if modify_door_id:
                try:
                    modify_door = ModifyDoors.objects.get(uuid=modify_door_id)
                    modify_door.site_status = 'WR'
                    modify_door.save()
                except ModifyDoors.DoesNotExist:
                    # Добавляем ошибку, но не откатываем транзакцию, так как услуги уже обновлены
                    errors.append({"error": f"Associated ModifyDoors not found: {modify_door_id}"})
                    return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response(updated_items, status=status.HTTP_200_OK)
