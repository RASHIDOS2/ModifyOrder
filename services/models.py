import uuid

from django.db import models

from orders.models import ModifyDoors


# Create your models here.
class Service(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, )
    title = models.CharField(max_length=255, null=True)
    size = models.CharField(max_length=255, null=True)
    angleCut = models.CharField(default=False)
    hinges = models.CharField(max_length=255)
    latchLeader = models.BooleanField(default=False)
    hole_lock = models.BooleanField(default=False)
    open_type = models.CharField(max_length=255)
    commentary = models.CharField(max_length=255, null=True)
    id_modify = models.ForeignKey(ModifyDoors, on_delete=models.CASCADE)


class Characteristics(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    title_nomenclature = models.CharField(max_length=255)
    title_characteristic = models.CharField(max_length=255)
    count = models.IntegerField(default=0)
    id_service = models.ForeignKey(Service, on_delete=models.CASCADE)
    id_modify = models.ForeignKey(ModifyDoors, on_delete=models.CASCADE)

