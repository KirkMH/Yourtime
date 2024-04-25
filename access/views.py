from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from client.models import Client
from joborder.models import JobOrder


@login_required
def dashboard(request):
    open_count = JobOrder.open_jobs.count()
    greeting = 'Good '

    current_hour = timezone.now().hour
    if 5 <= current_hour < 12:
        greeting += 'morning'
    elif 12 <= current_hour < 18:
        greeting += 'afternoon'
    else:
        greeting += 'evening'

    context = {
        'greeting': greeting,
        'clients': Client.objects.count(),
        'open_jo': open_count,
        'due_jo': JobOrder.open_jobs.filter(promise_date=timezone.now()).count(),
        'overdue': JobOrder.open_jobs.filter(promise_date__lt=timezone.now()).count(),
        'priority_jos': JobOrder.due_in_a_week.all()
    }
    return render(request, 'dashboard.html', context)
