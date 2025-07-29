import uuid

from django.db import models

# Create your models here.
class SiteOrderStatus(models.TextChoices):
    CREATE = 'CR', 'Создан'
    WRITE = 'WR', 'Записан'
    PROCESS = 'PR', 'В работе'
    CLOSE = 'CL', 'Закрыт'


class Orders(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=False)
    order_name = models.CharField(max_length=100)


class ModifyDoors(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    time_created = models.DateField(auto_now=False)
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    site_status = models.CharField(verbose_name="Статус заявки на сайте",
                                   max_length=10, choices=SiteOrderStatus.choices,
                                   default=SiteOrderStatus.CREATE)


