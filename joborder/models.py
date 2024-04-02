from django.db import models
from django.utils.translation import gettext_lazy as _

from client.models import Client
from access.models import Employee
from customization.models import (
    RepairWork,
    ModeOfPayment,
    Warranty,
    ItemCondition
)


class Articles(models.Manager):
    def get_queryset(self):
        return super().get_queryset().values('article').distinct()


class Dials(models.Manager):
    def get_queryset(self):
        return super().get_queryset().values('dial').distinct()


class WatchMovements(models.Manager):
    def get_queryset(self):
        return super().get_queryset().values('watch_movement').distinct()


class MovementCalibers(models.Manager):
    def get_queryset(self):
        return super().get_queryset().values('movement_caliber').distinct()


class Watch(models.Model):
    article = models.CharField(
        _("Article"),
        max_length=100,
        null=False, blank=False
    )
    serial_number = models.CharField(
        _("Serial Number"),
        max_length=100,
        null=False, blank=False
    )
    case_number = models.CharField(
        _("Case Number"),
        max_length=100,
        null=True, blank=True
    )
    dial = models.CharField(
        _("Dial"),
        max_length=100,
        null=True, blank=True
    )
    bracelet = models.CharField(
        _("Bracelet"),
        max_length=100,
        null=False, blank=False
    )
    components = models.CharField(
        _("Components"),
        max_length=100,
        null=False, blank=False
    )
    watch_movement = models.CharField(
        _("Watch Movement"),
        max_length=100,
        null=True, blank=True
    )
    movement_caliber = models.CharField(
        _("Movement Caliber"),
        max_length=100,
        null=True, blank=True
    )
    movement_number = models.CharField(
        _("Movement Number"),
        max_length=100,
        null=True, blank=True
    )
    aesthetic_defects = models.CharField(
        _("Aesthetic Defects"),
        max_length=254,
        null=True, blank=True
    )
    owner = models.ForeignKey(
        Client,
        verbose_name=_("Owner"),
        related_name="watch_owner",
        on_delete=models.CASCADE
    )
    for_him = models.BooleanField(
        _("For Him?"),
        default=True
    )
    for_her = models.BooleanField(
        _("For Her?"),
        default=True
    )

    objects = models.Manager()
    articles = Articles()
    dials = Dials()
    watch_movements = WatchMovements()
    movement_calibers = MovementCalibers()

    def __str__(self):
        str = f"{self.article.title()} SN#-{self.serial_number}"
        if self.case_number:
            str += f" Case#-{self.case_number}"
        return str


class JobOrder(models.Model):
    watch = models.ForeignKey(
        Watch,
        verbose_name=_("Watch"),
        related_name="watch_jo",
        on_delete=models.CASCADE
    )
    repair_work = models.ForeignKey(
        RepairWork,
        verbose_name=_("Repair Work"),
        related_name="repair_work_jo",
        on_delete=models.CASCADE
    )
    item_condition = models.ForeignKey(
        ItemCondition,
        verbose_name=_("Item Condition"),
        related_name="item_condition_jo",
        on_delete=models.CASCADE
    )
    assigned_technician = models.ForeignKey(
        Employee,
        verbose_name=_("Assigned Technician"),
        related_name="assigned_technician_jo",
        on_delete=models.CASCADE
    )
