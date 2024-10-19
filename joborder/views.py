from django.forms import BaseModelForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_serverside_datatable.views import ServerSideDatatableView
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .models import *
from .forms import *
from client.models import Client

objects = [
    {
        'type': 'watch',
        'model': Watch,
        'form': WatchForm,
        'description': 'Watch details',
        'tab_index': -1
    },
    {
        'type': 'joborder',
        'model': JobOrder,
        'form': JobOrderForm,
        'description': 'Job Order details',
        'tab_index': -1
    },
    {
        'type': 'assessment',
        'model': Assessment,
        'form': AssessmentForm,
        'description': 'Assessment details',
        'tab_index': 2
    },
    {
        'type': 'test',
        'model': TestLog,
        'form': TestLogForm,
        'description': 'Test Log details',
        'tab_index': 3
    },
    {
        'type': 'charge',
        'model': Charge,
        'form': ChargeForm,
        'description': 'Charge details',
        'tab_index': 4
    },
    {
        'type': 'arrival',
        'model': ArrivalPhoto,
        'form': ArrivalPhotoForm,
        'description': 'Arrival Photo',
        'tab_index': -1
    },
    {
        'type': 'release',
        'model': ReleasePhoto,
        'form': ReleasePhotoForm,
        'description': 'Release Photo',
        'tab_index': -1
    },
    {
        'type': 'payment',
        'model': Payment,
        'form': PaymentForm,
        'description': 'Payment details',
        'tab_index': 5
    }
]


def findObject(type):
    # find the type from the objects list and return the object if found, otherwise return None
    for obj in objects:
        if obj['type'] == type:
            return obj
    return None


def getModel(type):
    obj = findObject(type)
    if obj:
        return obj['model']
    return None


def getFormClass(type):
    obj = findObject(type)
    if obj:
        return obj['form']
    return None


def getDescription(type):
    obj = findObject(type)
    if obj:
        return obj['description']
    return None


def getTabIndex(type):
    obj = findObject(type)
    if obj:
        return obj['tab_index']
    return None


def addContext(context, type):
    if type == 'jo':
        context['conditions'] = ','.join(str(data['condition'])
                                         for data in JobOrder.conditions.all())
    elif type == 'watch':
        context['articles'] = ','.join(str(data['article'])
                                       for data in Watch.articles.all())
        context['dials'] = ','.join(str(data['dial'])
                                    for data in Watch.dials.all())
        context['bracelets'] = ','.join(str(data['bracelet'])
                                        for data in Watch.bracelets.all())
        context['components'] = ','.join(str(data['component'])
                                         for data in Watch.components.all())
        context['aesthetic_defects'] = ','.join(str(data['aesthetic_defect'])
                                                for data in Watch.aesthetic_defects.all())

    elif type == 'charge':
        context['particulars'] = ','.join(
            [str(particular) for particular in Particular.objects.all()])
    return context


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
               'client__tel_num', 'current_status', 'created_at', 'promise_date', 'watch__article']


@login_required
def create_jo(request):
    if request.method == 'POST':
        owner_id = request.POST.get('owner', None)
        owner = get_object_or_404(Client, pk=owner_id)
        if owner:
            jo = JobOrder.objects.create(
                client=owner
            )
            jo.save()
            messages.success(request, 'Job Order created successfully!')
            return redirect(reverse_lazy('jo_details', kwargs={'pk': jo.pk}))
    return redirect(reverse_lazy('jo_list'))


@login_required
def create_jo_from_client(request, pk):
    owner = get_object_or_404(Client, pk=pk)
    if owner:
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
        type = self.request.GET.get('type')
        index = getTabIndex(type)
        context = super().get_context_data(**kwargs)
        context['selected'] = index
        context['assessments'] = Assessment.objects.filter(
            job_order=self.object).order_by('-assessment_date')
        context['tests'] = TestLog.objects.filter(
            job_order=self.object).order_by('-tested_on')
        context['charges'] = Charge.objects.filter(
            job_order=self.object).order_by('-id')
        context['statuses'] = JO_STATUS
        context['arrivalphotos'] = ArrivalPhoto.objects.filter(
            job_order=self.object).order_by('id')
        context['releasephotos'] = ReleasePhoto.objects.filter(
            job_order=self.object).order_by('id')
        context['payments'] = Payment.objects.filter(
            job_order=self.object).order_by('id')
        return context


@method_decorator(login_required, name='dispatch')
class JobOrderWatchCreateView(CreateView):
    model = Watch
    form_class = WatchForm
    template_name = "joborder/jo_detail_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jo'] = get_object_or_404(JobOrder, pk=self.kwargs.get('pk'))
        context['type_name'] = 'Watch details'
        context = addContext(context, 'watch')
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
        jo = self.get_object()
        if type == 'watch':
            jo = jo.watch_jo
        elif type in ['assessment', 'test', 'charge']:
            jo = jo.job_order
        context['jo'] = jo
        context = addContext(context, type)
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

        elif type == 'charge':
            charge = form.save(commit=True)
            charge.addParticular()

        return super().form_valid(form)

    def get_success_url(self):
        type = self.request.GET.get('type')
        pk = self.get_object().pk
        if type == 'watch':
            pk = self.get_object().watch_jo.pk
        elif type in ['assessment', 'test', 'charge']:
            pk = self.get_object().job_order.pk
        messages.success(self.request, getDescription(
            type) + ' was updated successfully.')
        return reverse('jo_details', kwargs={'pk': pk}) + f'?type={type}'


@login_required
def save_estimate(request, pk):
    parts = float(request.POST.get('parts') or '0')
    serviceFee = float(request.POST.get('serviceFee') or '0')
    total = parts + serviceFee

    jo = get_object_or_404(JobOrder, pk=pk)
    estimate, _ = Estimate.objects.get_or_create(job_order=jo)
    estimate.parts = parts
    estimate.service_fee = serviceFee
    estimate.total_estimate = total
    estimate.save()

    return redirect(reverse('jo_details', kwargs={'pk': pk}))


@method_decorator(login_required, name='dispatch')
class JobOrderDocumentationCreateView(CreateView):
    template_name = "joborder/jo_detail_form.html"

    def get_model(self):
        type = self.request.GET.get('type')
        return getModel(type)

    def get_form_class(self):
        type = self.request.GET.get('type')
        return getFormClass(type)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type = self.request.GET.get('type')
        context['jo'] = get_object_or_404(JobOrder, pk=self.kwargs.get('pk'))
        context['type_name'] = getDescription(type)
        return addContext(context, type)

    def get_success_url(self):
        return reverse('jo_details', kwargs={'pk': self.kwargs.get('pk')}) + f"?type={self.request.GET['type']}"

    def form_valid(self, form):
        type = self.request.GET.get('type')
        jo = get_object_or_404(JobOrder, pk=self.kwargs.get('pk'))
        documentation = form.save(commit=False)
        documentation.job_order = jo
        if type == 'payment':
            emp = Employee.objects.filter(
                user=self.request.user)
            if emp.count() > 0:
                emp = emp.first()
            else:
                emp = None
            documentation.received_by = emp
        documentation.save()
        if type == 'charge':
            documentation.addParticular()
        messages.success(self.request, getDescription(
            type) + ' was added successfully.')
        return super().form_valid(form)


def update_jo_status(request, pk):
    status = request.POST.get('status')
    jo = get_object_or_404(JobOrder, pk=pk)
    jo.current_status = status
    jo.save()
    messages.success(request, 'Job Order status updated successfully!')
    return redirect(reverse('jo_details', kwargs={'pk': pk}))


def delete_photo(request, type, pk):
    photo = get_object_or_404(getModel(type), pk=pk)
    jo = photo.job_order
    photo.delete()
    messages.success(request, 'Photo deleted successfully!')
    return redirect(reverse('jo_details', kwargs={'pk': jo.pk}))
