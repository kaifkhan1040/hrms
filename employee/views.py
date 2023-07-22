from django.views.generic import View, FormView,ListView,CreateView,UpdateView,DeleteView
from .models import Bank
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.decorators import student_required,employee_required,superuser_required
from tablib import Dataset
from django.conf import settings
import csv
import os
from .forms import (
    BankForm
)

@method_decorator([login_required, superuser_required], name='dispatch')
class BankListView(LoginRequiredMixin,ListView):

    model = Bank
    paginate_by = 10  # if pagination is desired
    context_object_name = 'my_bank_list'

    def get_queryset(self):
        try:
            a = self.request.GET.get('bank', )
        except KeyError:
            a = None
        if a:
            bank_list = Bank.objects.filter(
                name__icontains=a,
            )
        else:
            bank_list = Bank.objects.filter()
        return bank_list

    def get_context_data(self, **kwargs):
        ctx = super(BankListView, self).get_context_data(**kwargs)
        ctx['pagetitle'] = 'RadintHRMS | Bank'
        #ctx['description'] = 'My Description'
        return ctx

    def dispatch(self, *args, **kwargs):
        return super(BankListView, self).dispatch(*args, **kwargs)

@method_decorator([login_required, superuser_required], name='dispatch')
class BankCreate(LoginRequiredMixin,CreateView):
    form_class = BankForm
    model = Bank
    success_url = reverse_lazy('common:bank')

    def get_context_data(self, **kwargs):
        context = super(BankCreate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Add Bank'
        return context

@method_decorator([login_required, superuser_required], name='dispatch')
class BankUpdate(LoginRequiredMixin,UpdateView):
    form_class = BankForm
    model = Bank
    success_url = reverse_lazy('common:bank')

    def get_context_data(self, **kwargs):
        context = super(BankUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Update Bank'
        return context

@method_decorator([login_required, superuser_required], name='dispatch')
class BankDelete(LoginRequiredMixin,DeleteView):
    model = Bank

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    success_url = reverse_lazy('common:bank')
