from django.db import models
from django.utils.translation import gettext_lazy as _


customization_status = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
)


class RepairWork(models.Model):
    description = models.CharField(
        _("Description"),
        max_length=254,
        null=False, blank=False
    )
    status = models.CharField(
        _("Status"),
        max_length=10,
        choices=customization_status,
        default='Active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description.title()
        ordering = ['description']


class ModeOfPayment(models.Model):
    description = models.CharField(
        _("Description"),
        max_length=254,
        null=False, blank=False
    )
    status = models.CharField(
        _("Status"),
        max_length=10,
        choices=customization_status,
        default='Active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description.title()

    class Meta:
        verbose_name_plural = "Modes of Payment"
        ordering = ['description']


class Warranty(models.Model):
    description = models.CharField(
        _("Description"),
        max_length=254,
        null=False, blank=False
    )
    status = models.CharField(
        _("Status"),
        max_length=10,
        choices=customization_status,
        default='Active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description.title()

    class Meta:
        verbose_name_plural = "Warranties"
        ordering = ['description']


class ExternalCaseAndBracelet(models.Model):
    description = models.CharField(
        _("Description"),
        max_length=254,
        null=False, blank=False
    )
    status = models.CharField(
        _("Status"),
        max_length=10,
        choices=customization_status,
        default='Active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description.title()

    class Meta:
        ordering = ['description']


class WatchMovement(models.Model):
    description = models.CharField(
        _("Description"),
        max_length=254,
        null=False, blank=False
    )
    status = models.CharField(
        _("Status"),
        max_length=10,
        choices=customization_status,
        default='Active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description.title()

    class Meta:
        ordering = ['description']


class WatchCaliber(models.Model):
    description = models.CharField(
        _("Description"),
        max_length=100,
        null=False, blank=False
    )
    service_charge = models.DecimalField(
        _("Service Charge"),
        max_digits=10,
        decimal_places=2,
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        _("Status"),
        max_length=10,
        choices=customization_status,
        default='Active'
    )

    def __str__(self):
        return self.description
