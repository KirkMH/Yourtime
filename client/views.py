from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_serverside_datatable.views import ServerSideDatatableView
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .models import Client
from .forms import *


###############################################################################################
#                Client Maintenance
###############################################################################################
@login_required
def client_list(request):
    return render(request, 'client/client_list.html')


@method_decorator(login_required, name='dispatch')
class ClientDTListView(ServerSideDatatableView):
    queryset = Client.objects.all()
    columns = ['pk', 'name', 'mob_num', 'tel_num', 'email']


@method_decorator(login_required, name='dispatch')
class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/client_form.html'

    def post(self, request, *args, **kwargs):
        form = ClientForm(request.POST)
        if form.is_valid():
            saved = form.save(commit=True)
            messages.success(request, f"{saved} was registered successfully.")
            if "another" in request.POST:
                return redirect('new_client')
            else:
                return redirect('create_jo_from_client', pk=saved.pk)

        else:
            return render(request, 'client/client_form.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class ClientUpdateView(SuccessMessageMixin, UpdateView):
    model = Client
    context_object_name = 'client'
    form_class = ClientUpdateForm
    template_name = "client/client_form.html"
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('client_list')
    success_message = "The client's record was updated successfully."


@method_decorator(login_required, name='dispatch')
class ClientDetailView(DetailView):
    model = Client
    template_name = "client/client_detail.html"
    context_object_name = 'client'


###############################################################################################
#                Client Inquiries
###############################################################################################
@login_required
def portal_list(request):
    return render(request, 'client/portal_list.html')


@method_decorator(login_required, name='dispatch')
class PortalDTListView(ServerSideDatatableView):
    queryset = Inquiry.objects.all()
    columns = ['pk', 'created_at', 'name', 'address', 'mob_num',
               'tel_num', 'email', 'issue', 'is_watch_owner']


@login_required
def portalDeleteView(request, pk):
    obj = get_object_or_404(Inquiry, pk=pk)
    obj.delete()
    messages.success(request, "The online inquiry was deleted successfully.")
    return redirect('portal_list')
