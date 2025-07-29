from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

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
