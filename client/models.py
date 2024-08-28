from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=254,
        null=False, blank=False
    )
    address = models.TextField()
    mob_num = models.CharField(
        _("Mobile Number"),
        max_length=100,
        null=False, blank=False)
    tel_num = models.CharField(
        _("Telephone Number"),
        max_length=100,
        null=True, blank=True)
    email = models.EmailField(
        _("Email Address"),
        max_length=254,
        null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name.title()

    def get_contact_info(self):
        contact = 'Contact Information: '
        if self.mob_num and self.tel_num:
            contact += f'{self.mob_num} | {self.tel_num}'
        elif self.mob_num:
            contact += f'{self.mob_num}'
        elif self.tel_num:
            contact += f'{self.tel_num}'
        return contact

    class Meta:
        ordering = ['name']
