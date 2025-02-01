from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from joborder.models import JobOrder, Payment
from client.models import Client
from access.models import Employee
from customization.models import ModeOfPayment


@login_required
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


@login_required
def client_report(request):
    clients = Client.objects.all()
    context = {
        'clients': clients,
    }
    return render(request, 'report/client_is.html', context=context)


@login_required
def job_order(request, pk, type):
    job_order = JobOrder.objects.get(pk=pk)
    context = {
        'joborder': job_order,
        'type': type.title(),
    }
    return render(request, 'report/job_order.html', context=context)


@login_required
def technician_metrics(request):
    technicians = Employee.technicians.all()
    context = {
        'technicians': technicians,
    }
    return render(request, 'report/tech_metrics.html', context=context)


@login_required
def collections_detailed(request):
    # get sel_from, and sel_to from the GET request
    sel_from = request.GET.get('from', None)
    sel_to = request.GET.get('to', None)
    print(f"sel_from: {sel_from}, sel_to: {sel_to}")

    collections = None
    total = 0
    if sel_from and sel_to:
        # generate from Payment model
        collections = Payment.objects.filter(
            date_paid__range=(sel_from, sel_to)
        ).order_by('date_paid')
        total = collections.aggregate(total=Sum('amount_paid'))['total']
        if collections.count() == 0:
            collections = 0
    print(f"collections: {collections}, total: {total}")

    context = {
        'sel_from': sel_from,
        'sel_to': sel_to,
        'collections': collections,
        'total': total
    }
    return render(request, 'report/collections_detailed.html', context=context)


@login_required
def collections_summary(request):
    # get sel_from, and sel_to from the GET request
    sel_from = request.GET.get('from', None)
    sel_to = request.GET.get('to', None)
    print(f"sel_from: {sel_from}, sel_to: {sel_to}")

    collections = []
    totals = None
    if sel_from and sel_to:
        # generate from Payment model
        totals = Payment.objects.filter(
            date_paid__range=(sel_from, sel_to)
        ).order_by('date_paid')

        # calculate totals group by date_paid and mode_of_payment
        totals = totals.values('date_paid', 'mode_of_payment').annotate(
            totals=Sum('amount_paid'))

    total = {}
    if totals:
        for t in totals:
            fmode = ModeOfPayment.objects.filter(id=t['mode_of_payment'])
            if fmode.exists():
                mode = fmode.first()
                mode_desc = mode.description.lower()
                # remove non-letter characters from mode_desc
                mode_desc = ''.join(filter(str.isalpha, mode_desc))
                total[mode_desc] = (total.get(mode_desc, 0)) + t['totals']
                total['subtotal'] = total.get('subtotal', 0) + t['totals']

                # check if the date exists in collections
                item = next(
                    (item for item in collections if item['date'] == t['date_paid']), None)
                if item:
                    item[mode_desc] = item.get(mode_desc, 0) + t['totals']
                    item['subtotal'] = item.get('subtotal', 0) + t['totals']
                else:
                    item = {}
                    item["date"] = t['date_paid']
                    item[mode_desc] = t['totals']
                    item['subtotal'] = t['totals']
                    collections.append(item)

    print(f"collections: {collections}, totals: {totals}")

    context = {
        'sel_from': sel_from,
        'sel_to': sel_to,
        'collections': collections,
        'total': total,
    }
    return render(request, 'report/collections_summary.html', context=context)


@login_required
def accounts_receivables(request):
    all_jo = JobOrder.objects.all().order_by('pk')
    # store all jo with balance > 0
    jo_with_balance = []
    total = {}
    for jo in all_jo:
        print(f"balance: {jo.balance()}\nstatus: {jo.current_status}")
        if jo.balance() > 0 and jo.current_status == 'FINISHED':
            jo_with_balance.append(jo)
            if jo.months_since_finished() <= 1:
                total["month1"] = total.get("month1", 0) + jo.balance()
            elif jo.months_since_finished() == 2:
                total["month2"] = total.get("month2", 0) + jo.balance()
            else:
                total["month3"] = total.get("month3", 0) + jo.balance()
    print(f"jo_with_balance: {jo_with_balance}, total: {total}")
    context = {
        'jo_with_balance': jo_with_balance,
        'total': total
    }
    return render(request, 'report/receivables.html', context)
