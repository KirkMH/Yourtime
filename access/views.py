from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import F, Sum

from client.models import Client
from joborder.models import JobOrder, Payment


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
