from django.shortcuts import render

from joborder.models import JobOrder
from client.models import Client


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
