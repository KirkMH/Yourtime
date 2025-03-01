from django.db import models

from django.contrib.auth.models import User
from joborder.models import JobOrder

from django.utils import timezone

# lists
userTypes = [
    (1, 'Technician'),
    (2, 'Encoders / Customer Service / Aftersales & Telemarketing'),
    (3, 'Parts Department'),
    (4, 'Inventory & Purchasing Department'),
    (5, 'Watch Security & Repair Coordinator'),
    (6, 'HR Department'),
    (7, 'Finance/Accounting'),
    (8, 'Operations Manager'),
    (9, 'Administrator')
]


class Technicians(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type=1).order_by('last_name').order_by('first_name')


class Employee(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
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

    def can_see_jo_completion(self):
        print(f"can_see_jo_completion user_type: {self.user_type}")
        return self.user_type >= 6

    def can_see_revenue(self):
        print(f"can_see_revenue user_type: {self.user_type}")
        return self.user_type >= 7

    def can_add_edit_jo(self):
        return self.user_type not in [2, 3, 6]

    def can_delete_jo(self):
        return self.user_type in [5, 9]

    def can_upload_photos(self):
        return self.user_type in [1, 2, 5, 8, 9]

    def can_assess_and_test(self):
        return self.user_type in [1, 5, 7, 8, 9]

    def can_charge_and_invoice(self):
        return self.user_type in [2, 3, 5, 7, 8, 9]

    def can_update_jo_status(self):
        return self.user_type in [1, 2, 5, 7, 8, 9]

    def can_manage_clients(self):
        return self.user_type in [2, 5, 7, 8, 9]

    def read_only_clients(self):
        return self.user_type in [7]

    def can_view_employees(self):
        return self.user_type in [6, 8, 9]

    def can_manage_users(self):
        return self.user_type in [9]

    def can_access_repair_works(self):
        return self.user_type not in [2, 6]

    def can_manage_repair_works(self):
        return self.user_type not in [2, 6, 7]

    def can_manage_parts_inventory(self):
        return self.user_type in [3, 4, 5, 8, 9]

    def can_access_payment_modes(self):
        return self.user_type in [2, 3, 5, 8, 9]

    def can_manage_payment_modes(self):
        return self.user_type in [3, 5, 8, 9]

    def can_access_warranties(self):
        return self.user_type in [2, 3, 5, 8, 9]

    def can_manage_warranties(self):
        return self.user_type in [3, 5, 8, 9]

    def can_manage_calibers(self):
        return self.user_type in [3, 5, 8, 9]

    def can_manage_movements(self):
        return self.user_type in [3, 5, 8, 9]

    def can_manage_externals(self):
        return self.user_type in [3, 5, 8, 9]

    def can_print(self):
        return self.user_type in [3, 4, 5, 6, 7, 8, 9]

    def can_view_daily_repairs(self):
        return self.user_type in [9]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
