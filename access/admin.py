from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import Group, User
from .models import Employee


# admin panel settings
admin.site.site_header = 'YourTime Center OPC Administrator'
admin.site.site_title = 'System Admin Area'
admin.site.index_title = 'YourTime Center OPC'


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class EmployeeAdminForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['user']
        widgets = {'features': forms.SelectMultiple()}


    # radio_fields = {"features": admin.VERTICAL}
EmployeeFormSet = inlineformset_factory(User, Employee, form=EmployeeAdminForm)


class EmployeeInline(admin.StackedInline):
    model = Employee
    formset = EmployeeFormSet
    can_delete = False
    verbose_name = _('Other Detail')


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name',
                    'last_login', 'is_active')
    inlines = (EmployeeInline, )

    fieldsets = (
        (None,
            {'fields': ('username', 'password')}),
        (_('Personal information'),
            {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'),
            {'fields': ('is_active', 'is_staff')}),
        (_('Important dates'),
            {'fields': ('last_login', 'date_joined')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("user_permissions", "user_groups")
        # Dynamically overriding
        self.fieldsets[2][1]["fields"] = ('is_active', 'is_staff')
        form = super(UserAdmin, self).get_form(request, obj, **kwargs)
        return form


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# remove unnecessary models from admin panel
admin.site.unregister(Group)
