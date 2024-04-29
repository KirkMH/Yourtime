from django.shortcuts import render

from joborder.models import JobOrder
from client.models import Client
from access.models import Employee


def due_report(request):
    type = request.GET.get('type')
    dues = JobOrder.overdues.all()
    if type == 'week':
        dues = JobOrder.due_in_a_week.all()
    context = {
        'dues': dues,
        'type': 'Past Due' if type == 'past' else 'Due in a Week',
    }
    return render(request, 'report/due.html', context=context)


def client_report(request):
    clients = Client.objects.all()
    context = {
        'clients': clients,
    }
    return render(request, 'report/client_is.html', context=context)


def job_order(request, pk, type):
    job_order = JobOrder.objects.get(pk=pk)
    context = {
        'joborder': job_order,
        'type': type.title(),
    }
    return render(request, 'report/job_order.html', context=context)


def technician_metrics(request):
    technicians = Employee.technicians.all()
    context = {
        'technicians': technicians,
    }
    return render(request, 'report/tech_metrics.html', context=context)
