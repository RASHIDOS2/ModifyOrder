import uuid

from django.db import models

from orders.models import ModifyDoors


# Create your models here.
class Service(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, )
    title = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    angleCut = models.CharField(default=False)
    hinges = models.CharField(max_length=255)
    latchLeader = models.BooleanField(default=False)
    hole_lock = models.BooleanField(default=False)
    id_modify = models.ForeignKey(ModifyDoors, on_delete=models.CASCADE)


class Characteristics(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False)
    title_nomenclature = models.CharField(max_length=255)
    title_characteristic = models.CharField(max_length=255)
    count = models.IntegerField(default=0)
    id_service = models.ForeignKey(Service, on_delete=models.CASCADE)
    id_modify = models.ForeignKey(ModifyDoors, on_delete=models.CASCADE)

