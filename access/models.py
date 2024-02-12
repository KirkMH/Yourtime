from django.db import models

from django.contrib.auth.models import User

# lists
userTypes = [
    (1, 'Technician'),
    (2, 'Asst. Head Technician'),
    (3, 'Head Technician'),
    (4, 'Manager'),
    (5, 'Administrator'),
]


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_type = models.IntegerField(choices=userTypes)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
