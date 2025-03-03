from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from joborder.models import JobOrder, Payment, JobOrderStatusUpdate
from client.models import Client
from access.models import Employee
from customization.models import ModeOfPayment
from datetime import datetime, date, timedelta
import calendar
from django.utils.timezone import make_aware


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
    last_month = date.today().replace(day=1) - timedelta(days=1)
    this_month = date.today().replace(day=1)
    context = {
        'technicians': technicians,
        'last_month': calendar.month_name[last_month.month],
        'this_month': calendar.month_name[this_month.month]
    }
    return render(request, 'report/tech_metrics.html', context=context)


def tech_job_order(request, pk):
    tech = Employee.objects.get(pk=pk)
    context = {
        'tech': tech
    }
    return render(request, 'report/tech_jo_list.html', context=context)


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
        'sel_from': datetime.strptime(sel_from, '%Y-%m-%d').date() if sel_from else None,
        'sel_to': datetime.strptime(sel_to, '%Y-%m-%d').date() if sel_to else None,
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
                mode_desc = mode.pk  # mode.description.lower()
                # remove non-letter characters from mode_desc
                # mode_desc = ''.join(filter(str.isalpha, mode_desc))
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
    modes = ModeOfPayment.objects.all().order_by('pk')
    # assign all pk of modes to indices variable
    indices = []
    for mode in modes:
        indices.append(mode.pk)
    print(f"modes: {modes}, indices: {indices}")

    context = {
        'sel_from': datetime.strptime(sel_from, '%Y-%m-%d').date() if sel_from else None,
        'sel_to': datetime.strptime(sel_to, '%Y-%m-%d').date() if sel_to else None,
        'collections': collections,
        'total': total,
        'modes': modes,
        'indices': indices
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


@login_required
def daily_repair(request):
    # get sel_from, and sel_type from the GET request
    sel_from = request.GET.get('from', None)
    sel_type = request.GET.get('type', None)
    print(f"sel_from: {type(sel_from)}, type: {sel_type}")

    repairs = None
    total_charges = 0
    total_payments = 0
    if sel_from and sel_type:
        sel_from = datetime.strptime(sel_from, '%Y-%m-%d').date()
        jo_status = sel_type
        if sel_type == 'Inflow':
            jo_status = 'SORTING'
        elif sel_type == 'Outflow':
            jo_status = 'CLAIMED'
        print(
            f'sel_from: {sel_from}, sel_type: {sel_type}, jo_status: {jo_status}')
        # from JobOrder record
        repairs_jo = JobOrder.objects.filter(
            created_at=sel_from,
            current_status=jo_status
        )
        print(f"repairs_jo: {repairs_jo}")
        repairs = repairs_jo.values_list('pk', flat=True)
        repairs_josu = JobOrderStatusUpdate.objects.extra(
            where=["DATE(updated_on) = %s"], params=[sel_from]).filter(status=jo_status)
        print(f"repairs_josu: {repairs_josu}")
        repairs = repairs.union(
            repairs_josu.values_list('job_order_id', flat=True))
        repairs = JobOrder.objects.filter(pk__in=repairs)
        # calculate total charges and total payments using the functions (not fields) total_charges and total_paid in JobOrder model
        total_payments = sum([r.total_paid() for r in repairs])
        total_charges = sum([r.total_charges() for r in repairs])
        if repairs.count() == 0:
            repairs = 0
    print(f"repairs: {repairs}, total_payments: {total_payments}")

    context = {
        'sel_from': sel_from if sel_from else None,
        'sel_type': sel_type,
        'repairs': repairs,
        'total_payments': total_payments,
        'total_charges': total_charges
    }
    print(f"context: {context}")
    return render(request, 'report/daily_repair.html', context=context)
