from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_serverside_datatable.views import ServerSideDatatableView
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .models import JobOrder, Watch, Estimate, Assessment
from .forms import WatchForm, JobOrderForm, AssessmentForm
from client.models import Client


def getModel(type):
    if type == 'watch':
        return Watch
    elif type == 'joborder':
        return JobOrder
    elif type == 'assessment':
        return Assessment
    return None


def getFormClass(type):
    if type == 'watch':
        return WatchForm
    elif type == 'joborder':
        return JobOrderForm
    elif type == 'assessment':
        return AssessmentForm
    return None


def getDescription(type):
    if type == 'watch':
        return 'Watch Details'
    elif type == 'joborder':
        return 'Job Order Details'
    elif type == 'assessment':
        return 'Assessment Details'


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assessments'] = Assessment.objects.filter(
            job_order=self.object).order_by('-assessment_date')
        print(f'Assessments: {context["assessments"]}')
        return context


@method_decorator(login_required, name='dispatch')
class JobOrderWatchCreateView(CreateView):
    model = Watch
    form_class = WatchForm
    template_name = "joborder/jo_detail_form.html"

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
        watch.job_order = jo
        watch.owner = jo.client
        watch.save()
        jo.watch = watch
        jo.save()

        estimate = None
        if Estimate.objects.filter(job_order=jo).exists():
            estimate = jo.estimate_jo
        else:
            estimate = Estimate.objects.create(job_order=jo)
        if watch.movement_caliber and watch.movement_caliber.service_charge:
            estimate.service_fee = watch.movement_caliber.service_charge
            estimate.total = estimate.parts + estimate.service_fee
            estimate.save()

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class JobOrderDetailUpdateView(UpdateView, SuccessMessageMixin):
    pk_url_kwarg = 'pk'
    template_name = "joborder/jo_detail_form.html"
    success_message = "The details was updated successfully."

    def get_model(self):
        type = self.request.GET.get('type')
        return getModel(type)

    def get_form_class(self):
        type = self.request.GET.get('type')
        return getFormClass(type)

    def get_queryset(self):
        model = self.get_model()
        return model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type = self.request.GET.get('type')
        context['type_name'] = getDescription(type)
        context['jo'] = self.get_object()
        if type == 'watch':
            context['jo'] = context['jo'].watch_jo
        elif type == 'assessment':
            context['jo'] = context['jo'].job_order
        return context

    def form_valid(self, form):
        type = self.request.GET.get('type')
        if type == 'watch':
            estimate = None
            watch = self.get_object()
            jo = watch.watch_jo
            if Estimate.objects.filter(job_order=jo).exists():
                estimate = jo.estimate_jo
            else:
                estimate = Estimate.objects.create(job_order=jo)
            if watch.movement_caliber and watch.movement_caliber.service_charge:
                estimate.service_fee = watch.movement_caliber.service_charge
                estimate.total = estimate.parts + estimate.service_fee
                estimate.save()

        elif type == 'assessment':
            form.save(commit=True)

        return super().form_valid(form)

    def get_success_url(self):
        type = self.request.GET.get('type')
        pk = self.get_object().pk
        if type == 'watch':
            pk = self.get_object().watch_jo.pk
        elif type == 'assessment':
            pk = self.get_object().job_order.pk
        return reverse('jo_details', kwargs={'pk': pk})


@login_required
def save_estimate(request, pk):
    parts = request.POST.get('parts') or 0
    serviceFee = request.POST.get('serviceFee') or 0
    total = parts + serviceFee

    jo = get_object_or_404(JobOrder, pk=pk)
    estimate = None
    if jo.estimate_jo:
        estimate = jo.estimate_jo
    else:
        estimate = Estimate.objects.create(job_order=jo)

    estimate.parts = parts
    estimate.service_fee = serviceFee
    estimate.total = total
    estimate.save()

    return redirect(reverse('jo_details', kwargs={'pk': pk}))


@method_decorator(login_required, name='dispatch')
class JobOrderAssessmentCreateView(CreateView):
    model = Assessment
    form_class = AssessmentForm
    template_name = "joborder/jo_detail_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jo'] = get_object_or_404(JobOrder, pk=self.kwargs.get('pk'))
        context['type_name'] = 'Assessment Details'
        return context

    def get_success_url(self):
        return reverse('jo_details', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        jo = get_object_or_404(JobOrder, pk=self.kwargs.get('pk'))
        assessment = form.save(commit=False)
        assessment.job_order = jo
        assessment.save()
        messages.success(self.request, 'Assessment was added successfully.')
        return super().form_valid(form)
