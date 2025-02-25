from django.db import models
from django.utils.translation import gettext_lazy as _


customization_status = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
)


class RepairWorkManager(models.Manager):
    def get_or_create(self, description):
        try:
            return self.get(description__icontains=description)
        except self.model.DoesNotExist:
            return self.create(description=description)


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

    objects = models.Manager()
    methods = RepairWorkManager()

    def __str__(self):
        return self.description.title()

    class Meta:
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


class WarrantyManager(models.Manager):
    def get_or_create(self, description):
        try:
            return self.get(description__icontains=description)
        except self.model.DoesNotExist:
            return self.create(description=description)


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

    objects = models.Manager()
    methods = WarrantyManager()

    def __str__(self):
        return self.description.title()

    class Meta:
        verbose_name_plural = "Warranties"
        ordering = ['description']


class ExternalCaseAndBraceletManager(models.Manager):
    def get_or_create(self, description):
        try:
            return self.get(description__icontains=description)
        except self.model.DoesNotExist:
            return self.create(description=description)


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

    objects = models.Manager()
    methods = ExternalCaseAndBraceletManager()

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


class BusinessSettings(models.Model):
    name = models.CharField(
        _("Business Name"),
        max_length=254,
        null=False, blank=False
    )
    address = models.TextField(
        _("Business Address"),
        null=False, blank=False
    )
    tel_num = models.CharField(
        _("Telephone Number"),
        max_length=15,
        null=False, blank=False
    )
    cp_num = models.CharField(
        _("CP Number"),
        max_length=15,
        null=False, blank=False
    )
    email = models.EmailField(
        _("Email Address"),
        null=False, blank=False
    )
    business_logo = models.ImageField(
        _("Business Logo"),
        upload_to="business_logo/",
        null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # Ensure only one instance exists
    def save(self, *args, **kwargs):
        self.pk = 1  # Force the primary key to always be 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # Prevent deletion of the single instance
