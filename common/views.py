from django.views.generic import View, FormView,ListView,CreateView,UpdateView,DeleteView
from .models import Country,State,City,Religion,Bank,Category,Department,Designation,Course
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
from .resources import CountryResource,StateResource,CityResource,ReligionResource,CategoryResource,BankResource,DepartmentResource,DesignationResource,CourseResource
from .forms import (
    CountryForm,StateForm,CityForm,ReligionForm,BankForm,CategoryForm,DepartmentForm,DesignationForm,CourseForm,
)

@method_decorator([login_required, superuser_required], name='dispatch')
class CountryListView(LoginRequiredMixin,ListView):

    model = Country
    paginate_by = 10  # if pagination is desired
    context_object_name = 'my_book_list'

    def get_queryset(self):
        try:
            a = self.request.GET.get('country', )
        except KeyError:
            a = None
        if a:
            country_list = Country.objects.filter(
                name__icontains=a,
                #owner=self.request.user
            )
        else:
            country_list = Country.objects.filter()
        return country_list

    def get_context_data(self, **kwargs):
        context = super(CountryListView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Country'
        return context

    def dispatch(self, *args, **kwargs):
        return super(CountryListView, self).dispatch(*args, **kwargs)


@method_decorator([login_required, superuser_required], name='dispatch')
class CountryCreate(LoginRequiredMixin,CreateView):
    form_class = CountryForm
    model = Country
    success_url = reverse_lazy('common:country')
    def get_context_data(self, **kwargs):
        context = super(CountryCreate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Add Country'
        return context

@method_decorator([login_required, superuser_required], name='dispatch')
class CountryUpdate(LoginRequiredMixin,UpdateView):
    form_class = CountryForm
    model = Country
    success_url = reverse_lazy('common:country')
    def get_context_data(self, **kwargs):
        context = super(CountryUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Update Country'
        return context

@method_decorator([login_required, superuser_required], name='dispatch')
class CountryDelete(LoginRequiredMixin,DeleteView):
    model = Country

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    success_url = reverse_lazy('common:country')


@method_decorator([login_required, superuser_required], name='dispatch')
class StateListView(LoginRequiredMixin,ListView):

    model = State
    paginate_by = 10  # if pagination is desired
    context_object_name = 'my_state_list'

    def get_queryset(self):
        try:
            a = self.request.GET.get('state', )
        except KeyError:
            a = None
        if a:
            state_list = State.objects.filter(
                name__icontains=a,
            )
        else:
            state_list = State.objects.filter()
        return state_list

    def dispatch(self, *args, **kwargs):
        return super(StateListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StateListView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | State'
        return context

@method_decorator([login_required, superuser_required], name='dispatch')
class StateCreate(LoginRequiredMixin,CreateView):
    form_class = StateForm
    model = State
    success_url = reverse_lazy('common:state')

    def get_context_data(self, **kwargs):
        context = super(StateCreate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Add State'
        return context

@method_decorator([login_required, superuser_required], name='dispatch')
class StateUpdate(LoginRequiredMixin,UpdateView):
    form_class = StateForm
    model = State
    success_url = reverse_lazy('common:state')

    def get_context_data(self, **kwargs):
        context = super(StateUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Update State'
        return context

@method_decorator([login_required, superuser_required], name='dispatch')
class StateDelete(LoginRequiredMixin,DeleteView):
    model = State

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    success_url = reverse_lazy('common:state')

@method_decorator([login_required, superuser_required], name='dispatch')
class CityListView(LoginRequiredMixin,ListView):

    model = City
    paginate_by = 10  # if pagination is desired
    context_object_name = 'my_city_list'

    def get_queryset(self):
        try:
            a = self.request.GET.get('city', )
        except KeyError:
            a = None
        if a:
            city_list = City.objects.filter(
                name__icontains=a,
                #owner=self.request.user
            )
        else:
            city_list = City.objects.filter()
        return city_list

    def dispatch(self, *args, **kwargs):
        return super(CityListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CityListView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | City'
        return context


@method_decorator([login_required, superuser_required], name='dispatch')
class CityCreate(LoginRequiredMixin,CreateView):
    form_class = CityForm
    model = City
    success_url = reverse_lazy('common:city')

    def get_context_data(self, **kwargs):
        context = super(CityCreate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Add City'
        return context

@method_decorator([login_required, superuser_required], name='dispatch')
class CityUpdate(LoginRequiredMixin,UpdateView):
    form_class = CityForm
    model = City
    success_url = reverse_lazy('common:city')

    def get_context_data(self, **kwargs):
        context = super(CityUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Update City'
        return context

@method_decorator([login_required, superuser_required], name='dispatch')
class CityDelete(LoginRequiredMixin,DeleteView):
    model = City

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    success_url = reverse_lazy('common:city')

@method_decorator([login_required, superuser_required], name='dispatch')
class ReligionListView(LoginRequiredMixin,ListView):

    model = Religion
    paginate_by = 10  # if pagination is desired
    context_object_name = 'my_religion_list'

    def get_queryset(self):
        try:
            a = self.request.GET.get('religion', )
        except KeyError:
            a = None
        if a:
            religion_list = Religion.objects.filter(
                name__icontains=a,
            )
        else:
            religion_list = Religion.objects.filter()
        return religion_list

    def dispatch(self, *args, **kwargs):
        return super(ReligionListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ReligionListView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Religion'
        return context

@method_decorator([login_required, superuser_required], name='dispatch')
class ReligionCreate(LoginRequiredMixin,CreateView):
    form_class = ReligionForm
    model = Religion
    success_url = reverse_lazy('common:religion')

    def get_context_data(self, **kwargs):
        context = super(ReligionCreate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Add Religion'
        return context

@method_decorator([login_required, superuser_required], name='dispatch')
class ReligionUpdate(LoginRequiredMixin,UpdateView):
    form_class = ReligionForm
    model = Religion
    success_url = reverse_lazy('common:religion')

    def get_context_data(self, **kwargs):
        context = super(ReligionUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Update Religion'
        return context

@method_decorator([login_required, superuser_required], name='dispatch')
class ReligionDelete(LoginRequiredMixin,DeleteView):
    model = Religion

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    success_url = reverse_lazy('common:religion')

@method_decorator([login_required, superuser_required], name='dispatch')
class CategoryListView(LoginRequiredMixin,ListView):

    model = Category
    paginate_by = 10  # if pagination is desired
    context_object_name = 'my_category_list'

    def get_queryset(self):
        try:
            a = self.request.GET.get('category', )
        except KeyError:
            a = None
        if a:
            category_list = Category.objects.filter(
                name__icontains=a,
            )
        else:
            category_list = Category.objects.filter()
        return category_list

    def dispatch(self, *args, **kwargs):
        return super(CategoryListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Category'
        return context

@method_decorator([login_required, superuser_required], name='dispatch')
class CategoryCreate(LoginRequiredMixin,CreateView):
    form_class = CategoryForm
    model = Category
    success_url = reverse_lazy('common:category')

    def get_context_data(self, **kwargs):
        context = super(CategoryCreate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Add Category'
        return context

@method_decorator([login_required, superuser_required], name='dispatch')
class CategoryUpdate(LoginRequiredMixin,UpdateView):
    form_class = CategoryForm
    model = Category
    success_url = reverse_lazy('common:category')

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Update Category'
        return context

@method_decorator([login_required, superuser_required], name='dispatch')
class CategoryDelete(LoginRequiredMixin,DeleteView):
    model = Category

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    success_url = reverse_lazy('common:category')

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

@method_decorator([login_required, superuser_required], name='dispatch')
class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    paginate_by = 10  # if pagination is desired
    context_object_name = 'my_department_list'
    def get_queryset(self):
        try:
            a = self.request.GET.get('department', )
        except KeyError:
            a = None
        if a:
            department_list = Department.objects.filter(
                name__icontains=a,
            )
        else:
            department_list = Department.objects.filter()
        return department_list
    def dispatch(self, *args, **kwargs):
        return super(DepartmentListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DepartmentListView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Department'
        return context

@method_decorator([login_required, superuser_required], name='dispatch')
class DepartmentCreate(LoginRequiredMixin, CreateView):
    form_class = DepartmentForm
    model = Department
    success_url = reverse_lazy('common:department')

    def get_context_data(self, **kwargs):
        context = super(DepartmentCreate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Add Department'
        return context

@method_decorator([login_required, superuser_required], name='dispatch')
class DepartmentUpdate(LoginRequiredMixin, UpdateView):
    form_class = DepartmentForm
    model = Department
    success_url = reverse_lazy('common:department')

    def get_context_data(self, **kwargs):
        context = super(DepartmentUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Update Department'
        return context

@method_decorator([login_required, superuser_required], name='dispatch')
class DepartmentDelete(LoginRequiredMixin, DeleteView):
    model = Department
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
        success_url = reverse_lazy('common:department')

@method_decorator([login_required, superuser_required], name='dispatch')
class DesignationListView(LoginRequiredMixin, ListView):
    model = Designation
    paginate_by = 10  # if pagination is desired
    context_object_name = 'my_designation_list'

    def get_queryset(self):
        try:
            a = self.request.GET.get('designation', )
        except KeyError:
            a = None
        if a:
            designation_list = Designation.objects.filter(
                name__icontains=a,
            )
        else:
            designation_list = Designation.objects.filter()
        return designation_list
    def dispatch(self, *args, **kwargs):
        return super(DesignationListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DesignationListView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Designation'
        return context

@method_decorator([login_required, superuser_required], name='dispatch')
class DesignationCreate(LoginRequiredMixin, CreateView):
        form_class = DesignationForm
        model = Designation
        success_url = reverse_lazy('common:designation')

        def get_context_data(self, **kwargs):
            context = super(DesignationCreate, self).get_context_data(**kwargs)
            context['pagetitle'] = 'RadiantHRMS | Add Designation'
            return context

@method_decorator([login_required, superuser_required], name='dispatch')
class DesignationUpdate(LoginRequiredMixin, UpdateView):
        form_class = DesignationForm
        model = Designation
        success_url = reverse_lazy('common:designation')

        def get_context_data(self, **kwargs):
            context = super(DesignationUpdate, self).get_context_data(**kwargs)
            context['pagetitle'] = 'RadiantHRMS | Update Designation'
            return context

@method_decorator([login_required, superuser_required], name='dispatch')
class DesignationDelete(LoginRequiredMixin, DeleteView):
        model = Designation
        def get(self, *args, **kwargs):
            return self.post(*args, **kwargs)
        success_url = reverse_lazy('common:designation')



@method_decorator([login_required, superuser_required], name='dispatch')
class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    paginate_by = 10  # if pagination is desired
    context_object_name = 'my_course_list'

    def get_queryset(self):
        try:
            a = self.request.GET.get('course', )
        except KeyError:
            a = None
        if a:
            course_list = Course.objects.filter(
                name__icontains=a,
            )
        else:
            course_list = Course.objects.filter()
        return course_list
    def dispatch(self, *args, **kwargs):
        return super(CourseListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Course'
        return context

@method_decorator([login_required, superuser_required], name='dispatch')
class CourseCreate(LoginRequiredMixin, CreateView):
        form_class = CourseForm
        model = Course
        success_url = reverse_lazy('common:course')

        def get_context_data(self, **kwargs):
            context = super(CourseCreate, self).get_context_data(**kwargs)
            context['pagetitle'] = 'RadiantHRMS | Add Course'
            return context

@method_decorator([login_required, superuser_required], name='dispatch')
class CourseUpdate(LoginRequiredMixin, UpdateView):
        form_class = CourseForm
        model = Course
        success_url = reverse_lazy('common:course')

        def get_context_data(self, **kwargs):
            context = super(CourseUpdate, self).get_context_data(**kwargs)
            context['pagetitle'] = 'RadiantHRMS | Update Course'
            return context

@method_decorator([login_required, superuser_required], name='dispatch')
class CourseDelete(LoginRequiredMixin, DeleteView):
        model = Course
        def get(self, *args, **kwargs):
            return self.post(*args, **kwargs)
        success_url = reverse_lazy('common:course')

@login_required
def export_country(request):
    country_resource = CountryResource()
    dataset = country_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="country.csv"'
    return response

@login_required
def export_state(request):
    state_resource = StateResource()
    dataset = state_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="state.csv"'
    return response

@login_required
def export_city(request):
    city_resource = CityResource()
    dataset = city_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="city.csv"'
    return response

@login_required
def export_religion(request):
    religion_resource = ReligionResource()
    dataset = religion_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="religion.csv"'
    return response

@login_required
def export_bank(request):
    bank_resource = BankResource()
    dataset = bank_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="bank.csv"'
    return response

@login_required
def export_category(request):
    category_resource = CategoryResource()
    dataset = category_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="category.csv"'
    return response

@login_required
def export_department(request):
    department_resource = DepartmentResource()
    dataset = department_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="department.csv"'
    return response

@login_required
def export_designation(request):
    designation_resource = DesignationResource()
    dataset = designation_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="designation.csv"'
    return response

@login_required
def export_course(request):
    course_resource = CourseResource()
    dataset = course_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="course.csv"'
    return response


@login_required
def import_country(request):
    if request.method == 'POST':
        country_resource = CountryResource()
        dataset = Dataset()
        new_countries = request.FILES['myfile']

        imported_data = dataset.load(new_countries.read().decode('utf-8'),format='csv')
        result = country_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            country_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'common/country_import.html',{'pagetitle':'RadiantHRMS | Country Import'})

@login_required
def import_state(request):
    if request.method == 'POST':
        state_resource = StateResource()
        dataset = Dataset()
        new_states = request.FILES['myfile']

        imported_data = dataset.load(new_states.read().decode('utf-8'), format='csv')
        result = state_resource.import_data(dataset, dry_run=True, raise_errors=True)  # Test the data import

        if not result.has_errors():
            state_resource.import_data(dataset, dry_run=False, raise_errors=True)  # Actually import now

    # chunk to write  into csv for import format
    DATA_ROOT = settings.DATA_ROOT
    os.rename(os.path.join(DATA_ROOT, 'format_state.csv'), os.path.join(DATA_ROOT, 'tmp_format_state.csv'))
    with open(os.path.join(DATA_ROOT, 'tmp_format_state.csv'), 'r', newline='') as rcsvfile:
        reader = csv.reader(rcsvfile)
        my_list = list(reader)
        with open(os.path.join(DATA_ROOT, 'format_state.csv'), 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile)
            cnt = Country.objects.all()
            k = 0
            for i in my_list:
                if k == 0:
                    i.append(' ')
                    for l in cnt:
                        i.append(l.name)
                filewriter.writerow(i)
                k = k + 1
    os.remove(os.path.join(DATA_ROOT, 'tmp_format_state.csv'))
    # chunk to write  into csv for import format

    return render(request, 'common/state_import.html',{'pagetitle':'RadiantHRMS | State Import'})

@login_required
def import_city(request):
    if request.method == 'POST':
        city_resource = CityResource()
        dataset = Dataset()
        new_cities = request.FILES['myfile']

        imported_data = dataset.load(new_cities.read().decode('utf-8'), format='csv')
        result = city_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            city_resource.import_data(dataset, dry_run=False)  # Actually import now
    # chunk to write  into csv for import format
    DATA_ROOT = settings.DATA_ROOT
    os.rename(os.path.join(DATA_ROOT, 'format_city.csv'), os.path.join(DATA_ROOT, 'tmp_format_city.csv'))
    with open(os.path.join(DATA_ROOT, 'tmp_format_city.csv'), 'r', newline='') as rcsvfile:
        reader = csv.reader(rcsvfile)
        my_list = list(reader)
        with open(os.path.join(DATA_ROOT, 'format_city.csv'), 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile)
            cnt = State.objects.all()
            k = 0
            for i in my_list:
                if k == 0:
                    i.append(' ')
                    for l in cnt:
                        i.append(l.name)
                filewriter.writerow(i)
                k = k + 1
    os.remove(os.path.join(DATA_ROOT, 'tmp_format_city.csv'))
    # chunk to write  into csv for import format

    return render(request, 'common/city_import.html',{'pagetitle':'RadiantHRMS | City Import'})

@login_required
def import_religion(request):
    if request.method == 'POST':
        religion_resource = ReligionResource()
        dataset = Dataset()
        new_religions = request.FILES['myfile']

        imported_data = dataset.load(new_religions.read().decode('utf-8'), format='csv')
        result = religion_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            religion_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'common/religion_import.html',{'pagetitle':'RadiantHRMS | Religion Import'})

@login_required
def import_bank(request):
    if request.method == 'POST':
        bank_resource = BankResource()
        dataset = Dataset()
        new_banks = request.FILES['myfile']

        imported_data = dataset.load(new_banks.read().decode('utf-8'), format='csv')
        result = bank_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            bank_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'common/bank_import.html',{'pagetitle':'RadiantHRMS | Bank Import'})

@login_required
def import_category(request):
    if request.method == 'POST':
        category_resource = CategoryResource()
        dataset = Dataset()
        new_categories= request.FILES['myfile']

        imported_data = dataset.load(new_categories.read().decode('utf-8'), format='csv')
        result = category_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            category_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'common/category_import.html',{'pagetitle':'RadiantHRMS | Category Import'})

@login_required
def import_department(request):
    if request.method == 'POST':
        department_resource = DepartmentResource()
        dataset = Dataset()
        new_departments = request.FILES['myfile']

        imported_data = dataset.load(new_departments.read().decode('utf-8'), format='csv')
        result = department_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            department_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'common/department_import.html',{'pagetitle':'RadiantHRMS | Department Import'})

@login_required
def import_designation(request):
    if request.method == 'POST':
        designation_resource = DesignationResource()
        dataset = Dataset()
        new_designations = request.FILES['myfile']

        imported_data = dataset.load(new_designations.read().decode('utf-8'), format='csv')
        result = designation_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            designation_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'common/designation_import.html',{'pagetitle':'RadiantHRMS | Designation Import'})


@login_required
def import_course(request):
    if request.method == 'POST':
        course_resource = CourseResource()
        dataset = Dataset()
        new_courses = request.FILES['myfile']

        imported_data = dataset.load(new_courses.read().decode('utf-8'), format='csv')
        result = course_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            course_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'common/course_import.html',{'pagetitle':'RadiantHRMS | Course Import'})