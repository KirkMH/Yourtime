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

features = [

  ('menu_dashboard', {
    "id": 1,
    "description": "Dashboard",
    "sub_of": None
  }),
  ('menu_search', {
    "id": 2,
    "description": "Search",
      "sub_of": None
  }),
  ('menu_records', {
    "id": 3,
    "description": "Records",
    "sub_of": None
  }),
  ("menu-jo", {
    "id": 4,
    "description": "Job Orders",
    "sub_of": "menu_records"
  }),
  ("photos-tab", {
    "id": 5,
    "description": "Photos",
    "sub_of": "menu_records menu-jo"
  }),
  ("estimate-tab", {
    "id": 6,
    "description": "Estimate",
    "sub_of": "menu_records menu-jo"
  }),
  ("assessments-tab", {
    "id": 7,
    "description": "Assessments",
    "sub_of": "menu_records menu-jo"
  }),
  ("tests-tab", {
    "id": 8,
    "description": "Test Logs",
    "sub_of": "menu_records menu-jo"
  }),
  ("charges-tab", {
    "id": 9,
    "description": "Charges",
    "sub_of": "menu_records menu-jo"
  }),
  ("payments-tab", {
    "id": 10,
    "description": "Payments",
    "sub_of": "menu_records menu-jo"
  }),
  ("receiving-tab", {
    "id": 11,
    "description":  "Receiving Report",
    "sub_of": "menu_records menu-jo"
  }),
  ("releasing-tab", {
    "id": 12,
    "description":  "Releasing Report",
    "sub_of": "menu_records menu-jo"
  }),
  ("menu-clients", {
    "id": 13,
    "description": "Clients",
    "sub_of": "menu_records"
  }),
  ("menu-portal", {
    "id": 14,
    "description": "Online Inquiry",
    "sub_of": "menu_records"
  }),
  ("menu-inquiry-logs", {
    "id": 15,
    "description": "Inquiry Logs",
    "sub_of": "menu_records"
  }),
  ("menu-reports", {
    "id": 16,
    "description": "Reports",
    "sub_of": None
  }),
  ("menu-past-due", {
    "id": 17,
    "description": "Past Due Job Orders",
    "sub_of": "menu-reports"
  }),
  ("menu-within-week", {
    "id": 18,
    "description": "Job Orders within the Week",
    "sub_of": "menu-reports"
  }),
  ("menu-daily-repair", {
    "id": 19,
    "description": "Daily Repair Report",
    "sub_of": "menu-reports"
  }),
  ("menu-client-info", {
    "id": 20,
    "description": "Client Information Sheet",
    "sub_of": "menu-reports"
  }),
  ("menu-metrics", {
    "id": 21,
    "description": "Technicians' Metrics",
    "sub_of": "menu-reports"
  }),
  ("menu-collections-detailed", {
    "id": 22,
    "description": "Detailed Collections",
    "sub_of": "menu-reports"
  }),
  ("menu-collections-summary", {
    "id": 23,
    "description": "Collections Summary",
    "sub_of": "menu-reports"
  }),
  ("menu-receivables", {
    "id": 24,
    "description": "Accounts Receivables",
    "sub_of": "menu-reports"
  }),
  ("menu-settings", {
    "id": 25,
    "description": "Settings",
    "sub_of": None
  }),
  ("menu-users", {
    "id": 26,
    "description": "Employees",
    "sub_of": "menu-settings"
  }),
  ("menu-repair-works", {
    "id": 27,
    "description": "Repair Works",
    "sub_of": "menu-settings"
  }),
  ("menu-item-externals", {
    "id": 28,
    "description": "External - Case and Bracelet",
    "sub_of": "menu-settings"
  }),
  ("menu-calibers", {
    "id": 29,
    "description": "Watch Calibers",
    "sub_of": "menu-settings"
  }),
  ("menu-movements", {
    "id": 30,
    "description": "Watch Movements",
    "sub_of": "menu-settings"
  }),
  ("menu-payment-modes", {
    "id": 31,
    "description": "Modes of Payment",
    "sub_of": "menu-settings"
  }),
  ("menu-warranties", {
    "id": 32,
    "description": "Warranties",
    "sub_of": "menu-settings"
  })
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

    def jo_completed_last_month(self):
        return JobOrder.objects.filter(assigned_technician=self, closed_at__month=timezone.localdate().month - 1)

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


class UserAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feature = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.feature}'