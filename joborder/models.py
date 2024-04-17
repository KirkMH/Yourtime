from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from client.models import Client
from access.models import Employee
from customization.models import (
    RepairWork,
    ModeOfPayment,
    Warranty,
    ExternalCaseAndBracelet,
    WatchCaliber,
    WatchMovement
)

JO_STATUS = [
    ('SORTING', 'Sorting'),
    ('IN-QUEUE', 'In Queue'),
    ('ONGOING', 'Ongoing'),
    ('OBSERVATION', 'Observation'),
    ('SAFEKEEPING', 'Safekeeping'),
    ('PENDING', 'Pending'),
    ('FOR-ESTIMATE', 'For Estimate'),
    ('UNCLAIMED', 'Unclaimed'),
    ('CLAIMED', 'Claimed'),
    ('PULLED-OUT', 'Pulled Out'),
    ('NOT-REPAIRABLE', 'Not Repairable'),
    ('IN-HOUSE', 'In House'),
    ('FINISHED', 'Finished')
]


class Articles(models.Manager):
    def get_queryset(self):
        return super().get_queryset().values('article').distinct()


class Dials(models.Manager):
    def get_queryset(self):
        return super().get_queryset().values('dial').distinct()


class Bracelets(models.Manager):
    def get_queryset(self):
        return super().get_queryset().values('bracelet').distinct()


class Components(models.Manager):
    def get_queryset(self):
        return super().get_queryset().values('component').distinct()


class AestheticDefects(models.Manager):
    def get_queryset(self):
        return super().get_queryset().values('aesthetic_defect').distinct()


class Watch(models.Model):
    article = models.CharField(
        _("Article"),
        max_length=100,
        null=False, blank=False
    )
    serial_number = models.CharField(
        _("Serial Number"),
        max_length=100,
        null=True, blank=True
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
        null=True, blank=True
    )
    component = models.CharField(
        _("Components"),
        max_length=100,
        null=True, blank=True
    )
    watch_movement = models.ForeignKey(
        WatchMovement,
        verbose_name=_("Watch Movement"),
        related_name="movement_watches",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    movement_caliber = models.ForeignKey(
        WatchCaliber,
        verbose_name=_("Movement Caliber"),
        related_name="caliber_watches",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    movement_number = models.CharField(
        _("Movement Number"),
        max_length=100,
        null=True, blank=True
    )
    aesthetic_defect = models.CharField(
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
    bracelets = Bracelets()
    components = Components()
    aesthetic_defects = AestheticDefects()

    def __str__(self):
        str = f"{self.article.title()} SN#-{self.serial_number}"
        if self.case_number:
            str += f" Case#-{self.case_number}"
        return str


class JobOrder(models.Model):
    client = models.ForeignKey(
        Client,
        verbose_name=_("Client"),
        related_name="client_jo",
        on_delete=models.CASCADE
    )
    watch = models.OneToOneField(
        Watch,
        verbose_name=_("Watch"),
        related_name="watch_jo",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    repair_work = models.ForeignKey(
        RepairWork,
        verbose_name=_("Repair Work"),
        related_name="repair_work_jo",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    notices = models.TextField(
        _("Notices"),
        null=True, blank=True
    )
    condition = models.CharField(
        _("Condition"),
        max_length=254,
        null=True, blank=True
    )
    external_case_and_bracelet = models.ForeignKey(
        ExternalCaseAndBracelet,
        verbose_name=_("External Case and Bracelet"),
        related_name="case_bracelet_jo",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    warranty = models.ForeignKey(
        Warranty,
        verbose_name=_("Warranty"),
        related_name="warranty",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    assigned_technician = models.ForeignKey(
        Employee,
        verbose_name=_("Assigned Technician"),
        related_name="assigned_technician_jo",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    current_status = models.CharField(
        _("Current Status"),
        max_length=25,
        choices=JO_STATUS,
        default='SORTING'
    )
    total_charges = models.DecimalField(
        _("Total Charges"),
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True, blank=True
    )
    total_paid = models.DecimalField(
        _("Total Paid"),
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True, blank=True
    )
    balance = models.DecimalField(
        _("Balance"),
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True, blank=True
    )
    created_at = models.DateField(auto_now_add=True)
    promise_date = models.DateField(
        _("Promise Date"),
        null=True, blank=True,
        default=timezone.now
    )


class Assessment(models.Model):
    job_order = models.ForeignKey(
        JobOrder,
        verbose_name=_("Job Order"),
        related_name="assessment_jo",
        on_delete=models.CASCADE
    )
    assessment = models.TextField(
        _("Assessment"),
        null=False, blank=False
    )
    assessment_date = models.DateField(
        _("Assessment Date"),
        null=False, blank=False
    )
    encoded_at = models.DateTimeField(auto_now_add=True)
    assessed_by = models.ForeignKey(
        Employee,
        verbose_name=_("Assessed By"),
        related_name="assessed_by",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.assessment


class TestLog(models.Model):
    job_order = models.ForeignKey(
        JobOrder,
        verbose_name=_("Job Order"),
        related_name="test_log_jo",
        on_delete=models.CASCADE
    )
    amplitude = models.PositiveIntegerField(
        _("Amplitude"),
        null=True, blank=True
    )
    comments = models.TextField(
        _("Comments"),
        null=True, blank=True
    )
    tested_on = models.DateTimeField(
        _("Tested On"),
        null=False, blank=False,
        default=timezone.now
    )
    tested_by = models.ForeignKey(
        Employee,
        verbose_name=_("Tested By"),
        related_name="tested_by",
        on_delete=models.CASCADE
    )
    encoded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Magnitude {self.amplitude}˚, {self.comments}'


class Particular(models.Model):
    description = models.CharField(
        _("Description"),
        max_length=254,
        null=False, blank=False
    )
    unit_price = models.DecimalField(
        _("Unit Price"),
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.description


class Charge(models.Model):
    job_order = models.ForeignKey(
        JobOrder,
        verbose_name=_("Job Order"),
        related_name="charge_jo",
        on_delete=models.CASCADE
    )
    particular = models.CharField(
        _("Particular"),
        max_length=254,
        null=False, blank=False
    )
    unit_price = models.DecimalField(
        _("Unit Price"),
        max_digits=10,
        decimal_places=2,
        default=0
    )
    quantity = models.PositiveIntegerField(
        _("Quantity"),
        default=1
    )
    total_amount = models.DecimalField(
        _("Total Amount"),
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f'{self.particular}, {self.quantity} x {self.unit_price} = {self.total_amount}'


class Estimate(models.Model):
    job_order = models.OneToOneField(
        JobOrder,
        verbose_name=_("Job Order"),
        related_name="estimate_jo",
        on_delete=models.CASCADE
    )
    service_fee = models.DecimalField(
        _("Service Fee"),
        max_digits=10,
        decimal_places=2,
        default=0
    )
    parts = models.DecimalField(
        _("Parts"),
        max_digits=10,
        decimal_places=2,
        default=0
    )
    total_estimate = models.DecimalField(
        _("Total Estimate"),
        max_digits=10,
        decimal_places=2,
        default=0
    )


class Payment(models.Model):
    job_order = models.ForeignKey(
        JobOrder,
        verbose_name=_("Job Order"),
        related_name="payment_jo",
        on_delete=models.CASCADE
    )
    mode_of_payment = models.ForeignKey(
        ModeOfPayment,
        verbose_name=_("Mode of Payment"),
        related_name="mode_of_payment",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    amount_paid = models.DecimalField(
        _("Amount Paid"),
        max_digits=10,
        decimal_places=2,
        default=0
    )
    or_number = models.PositiveIntegerField(
        _("OR Number"),
        null=True, blank=True
    )
    date_paid = models.DateField(
        _("Date Paid"),
        null=True, blank=True
    )
    received_by = models.ForeignKey(
        Employee,
        verbose_name=_("Received By"),
        related_name="received_by",
        on_delete=models.CASCADE
    )
