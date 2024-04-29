from django.db import models

from django.contrib.auth.models import User
from joborder.models import JobOrder

from django.utils import timezone

# lists
userTypes = [
    (1, 'Technician'),
    (2, 'Asst. Head Technician'),
    (3, 'Head Technician'),
    (4, 'Manager'),
    (5, 'Administrator'),
]


class Technicians(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type=1).order_by('last_name').order_by('first_name')


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_type = models.IntegerField(choices=userTypes)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()
    technicians = Technicians()

    def get_type_description(self):
        return dict(userTypes)[self.user_type]

    def get_delivery_performance_rating(self):
        jo_ontime = JobOrder.closed_on_time.filter(
            assigned_technician=self).count()
        jo_overdue = JobOrder.closed_late.filter(
            assigned_technician=self).count()
        total = jo_ontime + jo_overdue
        return (jo_ontime / total) * 100 if total > 0 else 0

    def ontime_job_orders(self):
        return JobOrder.closed_on_time.filter(assigned_technician=self)

    def overdue_job_orders(self):
        return JobOrder.closed_late.filter(assigned_technician=self)

    def jo_completed_within_the_month(self):
        return JobOrder.objects.filter(assigned_technician=self, closed_at__month=timezone.localdate().month)

    def active_jo(self):
        return JobOrder.objects.filter(assigned_technician=self, closed_at=None)

    def active_overdue(self):
        return JobOrder.objects.filter(assigned_technician=self, closed_at=None, promise_date__lt=timezone.localdate())

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
