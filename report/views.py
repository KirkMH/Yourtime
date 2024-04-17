from django.shortcuts import render

from joborder.models import JobOrder


def overdue_report(request):
    overdues = JobOrder.overdues.all()
    context = {
        'overdues': overdues,
    }
    return render(request, 'report/overdue.html', context=context)
