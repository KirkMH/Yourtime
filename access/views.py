from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import F, Sum, Q
from django.views.generic import ListView
from django.contrib import messages
from django.http import JsonResponse

from client.models import Client
from joborder.models import JobOrder, Payment
from django.contrib.auth.models import User
from .models import Employee
from .forms import *


@login_required
def search_page(request):
    err = None

    if request.method == 'POST':
        contact_no = request.POST.get('contact_no')
        jo_no = request.POST.get('jo_no')
        client_name = request.POST.get('client_name')

        if jo_no:
            # validate that jo_no is numeric
            if not jo_no.isdigit():
                err = "Job Order number must be numeric."
            else:
                query = JobOrder.objects.filter(pk=jo_no)
                if query:
                    return redirect('jo_details', pk=jo_no)
                else:
                    err = "Job Order number does not exist."
        else:
            query = Q()
            if contact_no:
                query |= Q(mob_num__contains=contact_no)
                query |= Q(tel_num__contains=contact_no)
            if client_name:
                query |= Q(name__contains=client_name)

            search_query = Client.objects.filter(query)
            print(search_query)
            context = {
                'contact_no': contact_no,
                'jo_no': jo_no,
                'client_name': client_name,
                'results': search_query
            }
            return render(request, 'search_results.html', context)

    return render(request, 'search.html', context={'err': err})


@login_required
def dashboard(request):
    open_count = JobOrder.open_jobs.count()
    greeting = 'Good '

    current_hour = timezone.localtime().hour
    if 5 <= current_hour < 12:
        greeting += 'morning'
    elif 12 <= current_hour < 18:
        greeting += 'afternoon'
    else:
        greeting += 'evening'

    # labels for the last 6 months
    labels = []
    jo_completion = []
    jo_ontime = []
    revenue = []
    for i in range(6):
        month = timezone.localtime() - timezone.timedelta(days=30 * (5 - i))
        label = month.strftime('%b %Y')
        # count completed job orders for this month
        completed_jo = JobOrder.objects.filter(
            closed_at__month=month.month,
            closed_at__year=month.year
        ).count()
        # count on-time job orders for this month, promise_date should be on or before the closed_at
        ontime_jo = JobOrder.objects.filter(
            closed_at__month=month.month,
            closed_at__year=month.year,
            promise_date__gte=F('closed_at')
        ).count()
        # calculate revenue for this month
        rev = Payment.objects.filter(
            job_order__closed_at__month=month.month,
            job_order__closed_at__year=month.year
        ).aggregate(total=Sum('amount_paid'))['total'] or 0

        labels.append(label)
        jo_completion.append(str(completed_jo))
        jo_ontime.append(str(ontime_jo))
        revenue.append(str(rev / 1000))

    context = {
        'greeting': greeting,
        'clients': Client.objects.count(),
        'open_jo': open_count,
        'due_jo': JobOrder.open_jobs.filter(promise_date=timezone.localdate()).count(),
        'overdue': JobOrder.open_jobs.filter(promise_date__lt=timezone.localdate()).count(),
        'priority_jos': JobOrder.due_in_a_week.all(),
        'labels': ",".join(labels),
        'jo_completion': ",".join(jo_completion),
        'jo_ontime': ",".join(jo_ontime),
        'revenue': ",".join(revenue),
    }
    return render(request, 'dashboard.html', context)


class EmployeeList(ListView):
    model = Employee
    template_name = 'settings/employee_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        return super().get_queryset()


@login_required
def employeeCreate(request):
    if request.method == 'POST':
        form = NewEmployeeForm(request.POST)
        if form.is_valid():
            user = None
            is_active = False
            if form.cleaned_data['username'] != "":
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password='YTOPCpassword123!'
                )
                is_active = True
            Employee.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                user_type=form.cleaned_data['user_type'],
                is_active=is_active
            )
            messages.success(request, "Employee was successfully created.")
            return redirect('employee_list')
    else:
        form = NewEmployeeForm()
    return render(request, 'settings/employee_form.html', {'form': form})


@login_required
def resetPassword(request, pk):
    employee = Employee.objects.get(pk=pk)
    employee.user.set_password('YTOPCpassword123!')
    employee.user.save()
    messages.success(request, "Password reset was successful.")
    return JsonResponse({'success': True})


@login_required
def removeAsUser(request, pk):
    employee = Employee.objects.get(pk=pk)
    user = employee.user
    user.delete()
    employee.user = None
    employee.is_active = False
    employee.save()
    messages.success(request, "Request was successful.")
    return JsonResponse({'success': True})


@login_required
def addAsUser(request, pk):
    username = request.GET.get('username')
    print(f"Username: {username}")
    user = User.objects.create_user(
        username=username,
        password='YTOPCpassword123!'
    )
    employee = Employee.objects.get(pk=pk)
    employee.user = user
    employee.is_active = True
    employee.save()
    messages.success(request, "Request was successful.")
    return JsonResponse({'success': True})


@login_required
def changeCredentials(request):
    # get currently logged in user
    employee = Employee.objects.get(user=request.user)

    if request.method == 'POST':
        form = UpdateEmployeeForm(request.POST)
        if form.is_valid():
            employee.first_name = form.cleaned_data['first_name']
            employee.last_name = form.cleaned_data['last_name']
            employee.save()
            messages.success(
                request, "Your credentials was successfully updated.")
            if form.cleaned_data['password'] != "":
                user = employee.user
                user.set_password(form.cleaned_data['password'])
                user.save()
                return redirect('logout')
    else:
        form = UpdateEmployeeForm(
            initial={'first_name': employee.first_name, 'last_name': employee.last_name})
    return render(request, 'settings/change_credentials.html', {'form': form})
