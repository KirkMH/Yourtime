from django.shortcuts import render

from joborder.models import JobOrder


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
