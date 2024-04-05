from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_serverside_datatable.views import ServerSideDatatableView
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers

from .models import JobOrder, Watch
from client.models import Client


@login_required
def jo_list(request):
    context = {
        'clients': Client.objects.all()
    }
    return render(request, 'joborder/jo_list.html', context=context)


@method_decorator(login_required, name='dispatch')
class JoDtListView(ServerSideDatatableView):
    queryset = JobOrder.objects.all()
    columns = ['pk', 'watch', 'client__name']


@login_required
def create_jo(request):
    if request.method == 'POST':
        owner_id = request.POST.get('owner', None)
        print(f'Owner ID: {owner_id}')
        owner = get_object_or_404(Client, pk=owner_id)
        if owner:
            print(f'Owner: {owner}')
            jo = JobOrder.objects.create(
                client=owner
            )
            jo.save()
            messages.success(request, 'Job Order created successfully!')
            return redirect(reverse_lazy('jo_details', kwargs={'pk': jo.pk}))
    return redirect(reverse_lazy('jo_list'))


@method_decorator(login_required, name='dispatch')
class JobOrderDetailView(DetailView):
    model = JobOrder
    template_name = "joborder/jo_detail.html"
    context_object_name = 'joborder'
