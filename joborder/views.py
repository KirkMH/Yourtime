from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_serverside_datatable.views import ServerSideDatatableView
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .models import JobOrder, Watch
from .forms import WatchForm
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
    columns = ['pk', 'watch__serial_number', 'client__name', 'client__mob_num',
               'client__tel_num', 'current_status', 'created_at', 'promise_date']


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


@method_decorator(login_required, name='dispatch')
class JobOrderWatchCreateView(CreateView):
    model = Watch
    form_class = WatchForm
    template_name = "joborder/jo_watch_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jo'] = get_object_or_404(JobOrder, pk=self.kwargs.get('pk'))
        print(f'joborder: {context["jo"].pk}')
        return context

    def get_success_url(self):
        return reverse('jo_details', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        jo = get_object_or_404(JobOrder, pk=self.kwargs.get('pk'))
        watch = form.save(commit=False)
        watch.joborder = jo
        watch.owner = jo.client
        watch.save()
        jo.watch = watch
        jo.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class JobOrderWatchUpdateView(UpdateView, SuccessMessageMixin):
    model = Watch
    form_class = WatchForm
    context_object_name = 'watch'
    pk_url_kwarg = 'pk'
    template_name = "joborder/jo_watch_form.html"
    success_message = "The watch details was updated successfully."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jo'] = self.get_object().watch_jo
        print(f'joborder: {context["jo"]}.pk')
        return context

    def get_success_url(self):
        return reverse('jo_details', kwargs={'pk': self.get_object().watch_jo.pk})
