from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_serverside_datatable.views import ServerSideDatatableView
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import Http404, QueryDict

from .models import RepairWork, ModeOfPayment, ItemCondition, Warranty
from .forms import create_setting_form, update_setting_form


valid_types = [('works', 'Repair Works'), ('conditions',
                                           'Item Conditions'), ('payments', 'Modes of Payment'),
               ('warranties', 'Warranties')]


def get_pair(type):
    pair = [pair for pair in valid_types if pair[0] == type]
    return pair[0] if pair else None


def get_model(type):
    if type == 'works':
        return RepairWork
    elif type == 'conditions':
        return ItemCondition
    elif type == 'payments':
        return ModeOfPayment
    elif type == 'warranties':
        return Warranty
    else:
        return None


@login_required
def setting_list(request):
    type = request.GET.get('type')
    pair = get_pair(type)
    if not pair:
        raise Http404("Page not found.")
    context = {
        'setting_code': pair[0],
        'setting_name': pair[1]
    }
    return render(request, 'settings/setting_list.html', context=context)


@method_decorator(login_required, name='dispatch')
class SettingDTListView(ServerSideDatatableView):
    columns = ['pk', 'description', 'status']

    def get_queryset(self):
        type = self.request.GET.get('type')
        model = get_model(type)
        if model:
            return model.objects.all()
        else:
            raise Http404("Page not found.")


@method_decorator(login_required, name='dispatch')
class SettingCreateView(CreateView):
    template_name = 'settings/setting_form.html'

    def get_model(self):
        type = self.request.GET.get('type')
        return get_model(type)

    def get_form_class(self):
        model = self.get_model()
        return create_setting_form(model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type = self.request.GET.get('type')
        pair = get_pair(type)

        context['setting_name'] = pair[1]
        context['setting_code'] = pair[0]
        return context

    def post(self, request, *args, **kwargs):
        type = request.GET.get('type')
        params = QueryDict(mutable=True)
        params['type'] = type
        model = get_model(type)
        setting_form = create_setting_form(model)
        form = setting_form(request.POST)
        if form.is_valid():
            saved = form.save(commit=True)
            messages.success(request, f"{saved} was registered successfully.")
            if "another" in request.POST:
                return redirect(reverse('new_setting_item') + f'?{params.urlencode()}')
            else:
                return redirect(reverse('setting_list') + f'?{params.urlencode()}')

        else:
            return render(request, 'client/client_form.html', {'form': form, 'type': type})


@method_decorator(login_required, name='dispatch')
class SettingUpdateView(SuccessMessageMixin, UpdateView):
    context_object_name = 'setting'
    pk_url_kwarg = 'pk'
    template_name = "settings/setting_form.html"
    success_url = reverse_lazy('setting_list')
    success_message = "The record was updated successfully."

    def get_model(self):
        type = self.request.GET.get('type')
        print('Type:', type)
        return get_model(type)

    def get_form_class(self):
        model = self.get_model()
        print('Model:', model)
        return update_setting_form(model)

    def get_queryset(self):
        model = self.get_model()
        return model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type = self.request.GET.get('type')
        pair = get_pair(type)

        context['setting_name'] = pair[1]
        context['setting_code'] = pair[0]
        return context

    def get_success_url(self):
        return super().get_success_url() + f'?type={self.request.GET.get("type")}'
