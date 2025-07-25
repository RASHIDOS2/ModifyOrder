from django.shortcuts import render
from rest_framework import viewsets

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

