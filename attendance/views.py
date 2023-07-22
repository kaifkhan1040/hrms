import glob

from geopy import GoogleV3
from geopy.geocoders import Nominatim
import json
import shutil
import datetime
import boto3
import geocoder as geocoder
import googlemaps as googlemaps
import requests
from botocore.exceptions import NoCredentialsError
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
import base64
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, UpdateView, DeleteView, CreateView


from .models import Attendance, Regularisation
from attendee.models import Employee, Student
from datetime import timedelta, datetime
from hierarchy.models import Branch, Batch, Holiday, Shifttime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.decorators import adminaccess_required
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from tablib import Dataset
from django.conf import settings
import os
import csv, logging
from .resources import StudentattendanceResource, EmployeeattendanceResource
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    EmployeeattendanceForm,
    RegularisationForm)
from django.contrib.auth import get_user_model

from app.conf.development.settings import CONTENT_DIR

from app.conf.development.settings import MEDIA_ROOT

from hierarchy.views import accessible_shifttime

User = get_user_model()
logger = logging.getLogger(__name__)

'''class AttendanceListView(ListView):
    model = Attendance
    paginate_by = 10  # if pagination is desired
    def get_queryset(self):
        try:
            a = self.request.GET.get('employee', )
        except KeyError:
            a = None
        if a:
            attendance_list = Attendance.objects.filter(
                user__email__icontains=a,
                user__is_employee__icontains=1
            )
        else:
            attendance_list = Attendance.objects.filter(user__is_employee__icontains=1)
        return attendance_list'''


@method_decorator([login_required], name='dispatch')
class MyregularisationListView(LoginRequiredMixin, ListView):
    model = Regularisation
    # paginate_by = 10  # if pagination is desired
    context_object_name = 'my_regularisation_data'
    template_name = 'attendance/myregularisation_list.html'

    def get_queryset(self, request=None):

        try:
            a = self.request.GET.get('regularisation', )
        except KeyError:
            a = None
        tmpEmpData = Employee.objects.get(user_id=self.request.user.id)

        if a:
            regularisation_list = Regularisation.objects.filter(reason=a, employee_id=tmpEmpData.id)
        else:
            regularisation_list = Regularisation.objects.filter(employee_id=tmpEmpData.id)
        return regularisation_list

    def dispatch(self, *args, **kwargs):
        return super(MyregularisationListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MyregularisationListView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | My Regularisation'
        return context


@method_decorator([login_required], name='dispatch')
class RegularisationListView(LoginRequiredMixin, ListView):
    model = Regularisation
    paginate_by = 25  # if pagination is desired
    context_object_name = 'my_regularisation_list'

    def get_queryset(self, request=None):
        try:
            a = self.request.GET.get('regularisation', )
        except KeyError:
            a = None

        regularisation_list = accessible_regularisation(self.request, a)
        return regularisation_list

    def dispatch(self, *args, **kwargs):
        return super(RegularisationListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RegularisationListView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Regularisation'
        return context


@method_decorator([login_required], name='dispatch')
class RegularisationCreate(LoginRequiredMixin, CreateView):
    form_class = RegularisationForm
    model = Regularisation
    success_url = reverse_lazy('attendance:regularisation')

    def form_valid(self, form):
        tmpemp = Employee.objects.filter(user_id=self.request.user.id)
        tmpbranch = Branch.objects.filter(id=tmpemp[0].branch_id)
        form.cleaned_data['Employee'] = tmpemp[0].id
        form.cleaned_data['Branch'] = tmpbranch[0].id
        obj = form.save(commit=False)
        obj.employee_id = tmpemp[0].id
        obj.branch_id = tmpbranch[0].id

        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(RegularisationCreate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Add Regularisation'
        return context


@method_decorator([login_required, adminaccess_required], name='dispatch')
class RegularisationUpdate(LoginRequiredMixin, UpdateView):
    form_class = RegularisationForm
    model = Regularisation
    success_url = reverse_lazy('attendance:regularisation')

    def get_context_data(self, **kwargs):
        context = super(RegularisationUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Update Regularisation'
        return context


@method_decorator([login_required, adminaccess_required], name='dispatch')
class RegularisationDelete(LoginRequiredMixin, DeleteView):
    model = Regularisation

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    success_url = reverse_lazy('attendance:regularisation')


# Ajax part of Regularisation ,but worst performance of laptop affecting my performance and it'll takes too much time for writing and performing any task .

def Ajaxupdate(request):
    # 0=> Pending, 1 => Rejected By RM , 2=> Rejected By HR, 3=> Approved By RM, 4=> Approved By RM and HR
    if request.method == 'GET':
        rawstatus = request.GET['status']
        rawid = request.GET['id']
        tmparr = str(rawid).split(',')
        logger.info(tmparr)
        adminaccessfor = request.session['adminfor']
        adminaccessforId = request.session['adminforId']

        if (rawstatus == 'accept' and (adminaccessfor == 'ce' or adminaccessfor == 'fr')):
            flagstatus = 4
        elif ((rawstatus == 'accept' and request.user.is_employee)):
            flagstatus = 3
        elif (rawstatus == 'reject' and (adminaccessfor == 'ce' or adminaccessfor == 'fr')):
            flagstatus = 2
        elif (rawstatus == 'reject' and request.user.is_employee):
            flagstatus = 1
        for k in tmparr:
            Regularisation.objects.filter(pk=k).update(status=flagstatus)

        result = {'Updated Successfully!!'}
        return HttpResponse(result)  # Sending an success response
    else:
        return HttpResponse("Request method is not a GET")


@login_required
def accessible_regularisation(request, searchString):
    uid = request.user.id
    try:
        eid = Employee.objects.get(user_id=uid)
    except Employee.DoesNotExist:
        raise ValidationError("user is not employee")
    adminaccessfor = request.session['adminfor']
    adminaccessforId = request.session['adminforId']

    getsubordinates = Employee.objects.filter(reporting_to_id=eid)
    regularisation_list = list
    if searchString and (adminaccessfor == 'fr' or adminaccessfor == 'ce') and adminaccessforId == eid.branch_id:
        regularisation_list = Regularisation.objects.filter(reason__icontains=searchString, branch_id=eid.branch_id,
                                                            status__gte=0)
    elif (adminaccessfor == 'fr' or adminaccessfor == 'ce') and adminaccessforId == eid.branch_id:
        regularisation_list = Regularisation.objects.filter(branch_id=eid.branch_id, status__gte=0)
    elif searchString and request.user.is_employee:
        regularisation_list = Regularisation.objects.filter(reason__icontains=searchString,
                                                            employee__in=getsubordinates, branch_id=eid.branch_id)
    elif request.user.is_employee:
        regularisation_list = Regularisation.objects.filter(employee__in=getsubordinates, branch_id=eid.branch_id)

    return regularisation_list


@method_decorator([login_required, adminaccess_required], name='dispatch')
class EmployeeattendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    paginate_by = 10  # if pagination is desired
    context_object_name = 'my_user_list'

    def get_queryset(self, fordate=None):
        return Attendance.objects.filter(fordate__gte='2020-01-01')

    def dispatch(self, *args, **kwargs):
        return super(EmployeeattendanceListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EmployeeattendanceListView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Employee Attendance'
        context['usertype'] = 'Employee'
        return context


@method_decorator([login_required, adminaccess_required], name='dispatch')
class EmployeeattendanceUpdate(LoginRequiredMixin, UpdateView):
    form_class = EmployeeattendanceForm
    model = Attendance
    success_url = reverse_lazy('attendance:employees')

    def form_valid(self, form):
        tid = 0
        ceid = form.cleaned_data.get('branch')

        self.object = form.save()
        # User.objects.filter(pk=self.object.user_id).update(editor_type=form.cleaned_data['admin_for'],editor_typeid=tid)
        # tmpUser.save()
        # form.instance.user_id=tmpUser.id

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(EmployeeattendanceUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Update Employee'
        context['usertype'] = 'Employee'
        return context


@method_decorator([login_required, adminaccess_required], name='dispatch')
class EmployeeattendanceDelete(LoginRequiredMixin, DeleteView):
    model = Attendance

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    success_url = reverse_lazy('attendance:employees')


@login_required
def export_employeeattendance(request):
    fdate = request.GET['fdate']
    tdate = request.GET['tdate']
    usersnamelike = request.GET['usersnamelike']
    selbranch = request.GET['selbranch']

    userlist = accessible_employeelist(request, usersnamelike)
    tmpuid = list()

    for ul in userlist:
        if selbranch:
            if int(ul.branch_id) == int(selbranch):
                tmpuid.append(ul.user_id)
        else:
            tmpuid.append(ul.user_id)

    employeeattendance_resource = EmployeeattendanceResource()
    queryset = Attendance.objects.filter(
        user_id__in=tmpuid,
        fordate__gte=fdate,
        fordate__lte=tdate)
    dataset = employeeattendance_resource.export(queryset)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="emp_attendance.csv"'
    return response


@login_required
def import_employeeattendance(request):
    if request.method == 'POST':
        employeeattendance_resource = EmployeeattendanceResource()
        dataset = Dataset()
        new_employees = request.FILES['myfile']

        imported_data = dataset.load(new_employees.read().decode('utf-8'), format='csv')
        result = employeeattendance_resource.import_data(dataset, dry_run=True,
                                                         raise_errors=True)  # Test the data import

        if not result.has_errors():
            employeeattendance_resource.import_data(dataset, dry_run=False)  # Actually import now

    # chunk to write  into csv for import format
    DATA_ROOT = settings.DATA_ROOT
    os.rename(os.path.join(DATA_ROOT, 'format_employeeattendance.csv'),
              os.path.join(DATA_ROOT, 'tmp_format_employeeattendance.csv'))
    with open(os.path.join(DATA_ROOT, 'tmp_format_employeeattendance.csv'), 'r', newline='') as rcsvfile:
        reader = csv.reader(rcsvfile)
        my_list = list(reader)
        with open(os.path.join(DATA_ROOT, 'format_employeeattendance.csv'), 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile)
            for i in my_list:
                filewriter.writerow(i)
    os.remove(os.path.join(DATA_ROOT, 'tmp_format_employeeattendance.csv'))
    # chunk to write  into csv for import format

    return render(request, 'attendance/employee_import.html', {'pagetitle': 'RadiantHRMS | Employee Attendance Import'})


@method_decorator([login_required, adminaccess_required], name='dispatch')
class StudentattendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    paginate_by = 10  # if pagination is desired
    context_object_name = 'my_user_list'

    '''def get_queryset(self):
        try:
            a = self.request.GET.get('student', )
        except KeyError:
            a = None
        if a:
            student_list = Attendance.objects.filter(
                user__email__icontains=a,
                user__is_student__icontains=1
            )
        else:
            student_list = Attendance.objects.filter(user__is_student__icontains=1)
        return student_list'''

    def dispatch(self, *args, **kwargs):
        return super(StudentattendanceListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StudentattendanceListView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Student Attendance'
        context['usertype'] = 'Student'
        return context


@method_decorator([login_required, adminaccess_required], name='dispatch')
class StudentattendanceUpdate(LoginRequiredMixin, UpdateView):
    form_class = EmployeeattendanceForm
    model = Attendance
    success_url = reverse_lazy('attendance:students')

    def form_valid(self, form):
        tid = 0
        ceid = form.cleaned_data.get('branch')

        self.object = form.save()
        # User.objects.filter(pk=self.object.user_id).update(editor_type=form.cleaned_data['admin_for'],editor_typeid=tid)
        # tmpUser.save()
        # form.instance.user_id=tmpUser.id

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(StudentattendanceUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Update Student Attendance'
        context['usertype'] = 'Student'
        return context


@method_decorator([login_required, adminaccess_required], name='dispatch')
class StudentattendanceDelete(LoginRequiredMixin, DeleteView):
    model = Attendance

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    success_url = reverse_lazy('attendance:students')


@login_required
def export_studentattendance(request):
    student_resource = StudentattendanceResource()
    dataset = student_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students_attendance.csv"'
    return response


@login_required
def import_studentattendance(request):
    if request.method == 'POST':
        employee_resource = EmployeeattendanceResource()
        dataset = Dataset()
        new_employees = request.FILES['myfile']

        imported_data = dataset.load(new_employees.read().decode('utf-8'), format='csv')
        result = employee_resource.import_data(dataset, dry_run=True, raise_errors=True)  # Test the data import

        if not result.has_errors():
            employee_resource.import_data(dataset, dry_run=False)  # Actually import now

    # chunk to write  into csv for import format
    DATA_ROOT = settings.DATA_ROOT
    os.rename(os.path.join(DATA_ROOT, 'format_studentattendance.csv'),
              os.path.join(DATA_ROOT, 'tmp_format_studentattendance.csv'))
    with open(os.path.join(DATA_ROOT, 'tmp_format_studentattendance.csv'), 'r', newline='') as rcsvfile:
        reader = csv.reader(rcsvfile)
        my_list = list(reader)
        with open(os.path.join(DATA_ROOT, 'format_studentattendance.csv'), 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile)
            for i in my_list:
                filewriter.writerow(i)
    os.remove(os.path.join(DATA_ROOT, 'tmp_format_studentattendance.csv'))
    # chunk to write  into csv for import format

    return render(request, 'attendance/student_import.html', {'pagetitle': 'RadiantHRMS | Student Attendance Import'})


def AjaxList(request):
    if request.method == 'GET':
        fromdate = request.GET['fromdate']
        todate = request.GET['todate']
        aemail = request.GET['aemail']
        usertypes = request.GET['utype']
        usersnamelike = request.GET['usersnamelike']
        selbranch = request.GET['selbranch']

        if (usertypes == 'Employee'):
            userlist = accessible_employeelist(request, usersnamelike)
            role = 'employees'
        else:
            userlist = accessible_studentlist(request, usersnamelike)
            role = 'students'
        tmpuid = list()

        for ul in userlist:
            if selbranch:
                if int(ul.branch_id) == int(selbranch):
                    tmpuid.append(ul.user_id)
            else:
                tmpuid.append(ul.user_id)

        attendance_list = Attendance.objects.filter(
            user_id__in=tmpuid,
            fordate__gte=fromdate,
            fordate__lte=todate
        )

        htmldata = '<thead><tr><th>#</th><th>User Name</th><th>Email Id</th><th>Date</th><th>InTime</th><th>OutTime</th><th>Lattitude</th><th>Longitude</th><th>Action</th></tr></thead><tbody>'
        k = 1
        msg = "'Are You Sure!!!'"
        if len(attendance_list) > 0:
            for i in attendance_list:
                htmldata += '<tr><td>' + str(k) + '</td><td></td><td>' + i.user.email + '</td><td>' + str(
                    i.fordate) + '</td><td>' + str(i.event_hh) + ':' + str(i.event_mm) + '</td><td>' + str(
                    i.event_hh) + ':' + str(i.event_mm) + '</td><td>' + str(i.lattitude) + '</td><td>' + str(
                    i.longitude) + ' </td><td><a href = "/attendance/' + role + '/edit/' + str(
                    i.id) + '"> <i class ="fa fa-pencil" style="color:green"> </i></a> | <a onclick="return confirm(' + msg + ')" href="/attendance/' + role + '/delete/' + str(
                    i.id) + '" > <i class ="fa fa-trash" style="color:red" > </i> </a></td></tr>'
                k = k + 1
        else:
            htmldata += '<tr><td>Nothing to show!!!</td></tr>'
        htmldata += '</tbody></html>'
        result = htmldata
        return HttpResponse(result)  # Sending an success response
    else:
        return HttpResponse("Request method is not a GET")


@login_required
def accessible_branchlist(request):
    adminaccessfor = request.session['adminfor']
    adminaccessforId = request.session['adminforId']
    if request.user.is_superuser:
        branch_list = Branch.objects.filter()
    elif adminaccessfor == 'ce':
        branch_list = Branch.objects.filter(pk=adminaccessforId)
    elif adminaccessfor == 'fr':
        branch_list = Branch.objects.filter(organisation_id=adminaccessforId)
    return branch_list


@login_required
def accessible_batchlist(request):
    adminaccessfor = request.session['adminfor']
    adminaccessforId = request.session['adminforId']
    clist = accessible_branchlist(request)
    if request.user.is_superuser:
        batch_list = Batch.objects.filter()
    elif adminaccessfor == 'ce' or adminaccessfor == 'fr':
        batch_list = Batch.objects.filter(branch__in=clist)
    return batch_list


@login_required
def accessible_employeelist(request, searchString, eid=None):
    adminaccessfor = request.session['adminfor']
    # adminaccessforId = request.session['adminforId']
    clist = accessible_shifttime(request, '')
    if eid:
        employee_list = Employee.objects.filter(pk=eid)
    elif searchString and request.user.is_superuser:
        employee_list = Employee.objects.filter(first_name__icontains=searchString)
    elif request.user.is_superuser:
        employee_list = Employee.objects.filter()
    elif adminaccessfor == 'ce' or adminaccessfor == 'fr':
        employee_list = Employee.objects.filter(shifttime__in=clist)

    return employee_list


@login_required
def accessible_studentlist(request, searchString):
    adminaccessfor = request.session['adminfor']
    adminaccessforId = request.session['adminforId']
    clist = accessible_branchlist(request)
    if searchString and request.user.is_superuser:
        student_list = Student.objects.filter(first_name__icontains=searchString)
    elif request.user.is_superuser:
        student_list = Student.objects.filter()
    elif adminaccessfor == 'ce' or adminaccessfor == 'fr':
        student_list = Student.objects.filter(branch__in=clist)
    return student_list


def load_employees(request):
    utype = request.GET['usertype']
    if utype == 'Student':
        entities = accessible_studentlist(request, '')
    elif utype == 'Employee':
        entities = accessible_employeelist(request, '')
    selectedItem = request.GET['su']
    if not selectedItem:
        selectedItem = 0
    return render(request, 'attendance/entity_dropdown_list_options.html',
                  {'entities': entities, 'selectedItem': int(selectedItem)})


def attendance_report(request):
    return render(request, 'attendance/entity_report_list.html', {})


def load_reports(request):
    try:
        utype = request.GET['utype']
        #branch = request.GET['selbranch']
        shifttime = request.GET['selshifttime']

        fromdate = request.GET['fromdate']
        todate = request.GET['todate']
        batch = request.GET['selbatch']
        employeeid = request.GET['selemployee']
    except:
        raise KeyError("please send args like utype,selshifttime ,fromdate , todate, selbatch ,selemployee")

    if request.method == 'GET':
        search_query = request.GET.get('search_box', None)

    if utype == 'Student':
        entities = accessible_studentlist(request, '')
    elif utype == 'Employee':
        entities = accessible_employeelist(request, '', (employeeid))

    # filter by branch/batch
    usersList = list()
    usersIdList = ''
    for j in entities:
        if(((utype == 'Employee') and (int(j.shifttime_id) == int(shifttime)) and (j.status) == 1)  or (
                (utype == 'Student') and (int(j.batch_id) == int(batch)))):
            if (j.user_id):
                usersList.append(j)
                usersIdList += str(j.user_id) + ','

    sdate = datetime.strptime(fromdate, '%Y-%m-%d')  # start date
    edate = datetime.strptime(todate, '%Y-%m-%d')  # end date
    delta = edate - sdate  # as timedelta
    userlist = {}
    ulist = list()
    hlist = list()
    weekofflist = list()
    # shiftlist = list()
    holidaylist = list()
    hduration = 0
    for a in usersList:
        ulist.append(a.first_name)
        # weekofflist
        if utype == 'Student':
            weekoffs = Batch.objects.filter(
                id=a.batch_id
            )
        elif utype == 'Employee':
            weekoffs = Shifttime.objects.filter(
                id=a.shifttime_id
            ).order_by('end_time_type')

        if (weekoffs[0].week_off1):
            weekofflist.append(weekoffs[0].week_off1)
        if (weekoffs[0].week_off2):
            weekofflist.append(weekoffs[0].week_off2)
        if (weekoffs[0].week_off3):
            weekofflist.append(weekoffs[0].week_off3)
        if (weekoffs[0].week_off4):
            weekofflist.append(weekoffs[0].week_off4)
        if (weekoffs[0].week_off5):
            weekofflist.append(weekoffs[0].week_off5)
        minduration = weekoffs[0].min_duration_required

        # holidaylist
        holidays = Holiday.objects.filter(branch_id=a.branch_id)
        for hd in holidays:
            holidaylist.append(hd.hdate.strftime('%Y-%m-%d'))

        tmplist = list()
        datelist = list()
        datelist1 = list()
        analyticsHolidayCount = 0
        analyticsWeekoffCount = 0
        analyticsWorkingdayCount = 0
        for b in range(delta.days + 1):
            day = sdate + timedelta(days=b)
            qdate = str(day)[0:10]

            # nextday = qdate + timedelta(days=1)
            # qdate1 = str(nextday)[0:10]

            '''attendancelist=Attendance.objects.filter(
                user_id=a.user_id,
                fordate=qdate'
            )'''

            attendancelist = Attendance.objects.raw(
                "SELECT id,user_id,fordate,address as ads,event_hh as eh,event_mm as em,event_ss as es FROM attendance_attendance where fordate='" + qdate + "' and user_id='" + str(
                    a.user_id) + "' order by event_hh,event_mm limit 1")

            attendancelist1 = Attendance.objects.raw(
                "SELECT id,user_id,fordate,address as ads,event_hh as eh,event_mm as em,event_ss as es FROM attendance_attendance where fordate='" + qdate + "' and user_id='" + str(
                    a.user_id) + "' order by event_hh desc,event_mm desc limit 1")

            datelist.append(datetime.strptime(qdate, '%Y-%m-%d').strftime('%d%b`%y'))
            datelist1.append(qdate)

            if qdate in holidaylist:
                analyticsHolidayCount = analyticsHolidayCount + 1
                tmplist.append({qdate: 'H'})
            elif day.weekday() in weekofflist:
                analyticsWeekoffCount = analyticsWeekoffCount + 1
                tmplist.append({qdate: 'WO'})

            elif attendancelist and attendancelist1 and weekoffs[0].end_time_type == 1:
                analyticsWorkingdayCount = analyticsWorkingdayCount + 1

                duration = 0

                batchStartTime = str(weekoffs[0].start_time_hh).zfill(2) + str(weekoffs[0].start_time_mm).zfill(2)
                batchEndTime = str(weekoffs[0].end_time_hh).zfill(2) + str(weekoffs[0].end_time_mm).zfill(2)
                candidateStartTime = str(attendancelist[0].eh).zfill(2) + str(attendancelist[0].em).zfill(
                    2)

                candidateEndTime = str(attendancelist1[0].eh).zfill(2) + str(attendancelist1[0].em).zfill(
                    2)

                finalstarthour = int(attendancelist[0].eh)
                finalstartmin = int(attendancelist[0].em)
                finalendhour = int(attendancelist1[0].eh)
                finalendmin = int(attendancelist1[0].em)


                if (int(candidateStartTime) < int(batchStartTime)):
                    finalstarthour = int(weekoffs[0].start_time_hh)
                    finalstartmin = int(weekoffs[0].start_time_mm)
                if (int(candidateEndTime) > int(batchEndTime)):
                    finalendhour = int(weekoffs[0].start_time_hh)
                    finalendmin = int(weekoffs[0].start_time_mm)

                finalStartTmp = finalstarthour * 60 + finalstartmin
                finalEndTmp = finalendhour * 60 + finalendmin
                proDuration = int(finalEndTmp) - int(finalStartTmp)
                shortExtra = proDuration - minduration
                # startx = attendancelist[0].intime_hh * 60 + attendancelist[0].intime_mm
                # endx = attendancelist[0].outtime_hh * 60 + attendancelist[0].outtime_mm
                # duration = endx - startx
                # if duration < 0:
                #    duration = duration + 1440
                # duration_diff = minduration - duration
                duration = "{0:.2f}".format(proDuration / 60)
                hduration = duration
                duration_diff = "{0:.2f}".format((shortExtra / 60))
                duration_diff1 = "{0:.2f}".format((shortExtra / 60))
                if (float(duration_diff1) >= 0):
                    moreless = ' Extra(' + str(abs(float(duration_diff))) + 'hrs)'
                else:
                    moreless = ' Short(' + str(abs(float(duration_diff))) + 'hrs)'
                if int(attendancelist[0].eh) < 10:
                    attendancelist[0].eh = '0' + str(attendancelist[0].eh)
                if int(attendancelist1[0].eh) < 10:
                    attendancelist1[0].eh = '0' + str(attendancelist1[0].eh)
                if int(attendancelist[0].em) < 10:
                    attendancelist[0].em = '0' + str(attendancelist[0].em)
                if int(attendancelist1[0].em) < 10:
                    attendancelist1[0].em = '0' + str(attendancelist1[0].em)
                tmplist.append({qdate: 'InTime-' + str(attendancelist[0].eh) + ':' + str(
                    attendancelist[0].em) +
                    'OutTime-' + str(attendancelist1[0].eh) + ':' + str(attendancelist1[0].em) +
                    'Duration(' + str(duration) + 'hrs)' + moreless +
                    'CurrentLoc-In-' + str(attendancelist[0].ads) + 'CurrentLoc-Out-' + str(attendancelist1[0].ads)
                    })


            elif weekoffs[0].end_time_type == 2:
                shift_start = weekoffs[0].start_time_hh - 1
                shift_end = weekoffs[0].end_time_hh + 5
                tmpday = sdate + timedelta(days=b + 1)
                nextqdate = str(tmpday)[0:10]

                attendancelistin = Attendance.objects.raw(
                    "SELECT id,user_id,fordate,address as ads,event_hh as eh,event_mm as em,event_ss as es FROM attendance_attendance where fordate='" + qdate + "' and event_hh >=' " + str(
                        shift_start) + "' and   user_id='" + str(
                        a.user_id) + "' order by event_hh,event_mm limit 1")
                logger.info(attendancelistin)
                attendancelistout = Attendance.objects.raw(
                    "SELECT id,user_id,fordate,address as ads,event_hh as eh,event_mm as em,event_ss as es FROM attendance_attendance where fordate='" + nextqdate + "' and event_hh <' " + str(
                        shift_end) + "' and  user_id='" + str(
                        a.user_id) + "' order by event_hh desc,event_mm desc limit 1")
                logger.info(attendancelistout)

                if attendancelistin and attendancelistout:

                    analyticsWorkingdayCount = analyticsWorkingdayCount + 1

                    duration = 0

                    batchStartTime = str(weekoffs[0].start_time_hh).zfill(2) + str(weekoffs[0].start_time_mm).zfill(2)
                    batchEndTime = str(weekoffs[0].end_time_hh).zfill(2) + str(weekoffs[0].end_time_mm).zfill(2)
                    candidateStartTime = str(attendancelistin[0].eh).zfill(2) + str(attendancelistin[0].em).zfill(
                        2)

                    candidateEndTime = str(attendancelistout[0].eh).zfill(2) + str(attendancelistout[0].em).zfill(
                        2)

                    finalstarthour = int(attendancelistin[0].eh)
                    finalstartmin = int(attendancelistin[0].em)
                    finalendhour = int(attendancelistout[0].eh)
                    finalendmin = int(attendancelistout[0].em)

                    '''if (int(candidateStartTime) < int(batchStartTime)):
                        finalstarthour = int(weekoffs[0].start_time_hh)
                        finalstartmin = int(weekoffs[0].start_time_mm)
                    if (int(candidateEndTime) > int(batchEndTime)):
                        finalendhour = int(weekoffs[0].start_time_hh)
                        finalendmin = int(weekoffs[0].start_time_mm)'''

                    finalStartTmp = 1440 - (finalstarthour * 60 + finalstartmin)
                    finalEndTmp = finalendhour * 60 + finalendmin
                    proDuration = int(finalEndTmp) + int(finalStartTmp)
                    shortExtra = proDuration - minduration
                    # startx = attendancelist[0].intime_hh * 60 + attendancelist[0].intime_mm
                    # endx = attendancelist[0].outtime_hh * 60 + attendancelist[0].outtime_mm
                    # duration = endx - startx
                    # if duration < 0:
                    #    duration = duration + 1440
                    # duration_diff = minduration - duration
                    duration = "{0:.2f}".format(proDuration / 60)
                    hduration = duration
                    duration_diff = "{0:.2f}".format((shortExtra / 60))
                    duration_diff1 = "{0:.2f}".format((shortExtra / 60))
                    if (float(duration_diff1) >= 0):
                        moreless = ' Extra(' + str(abs(float(duration_diff))) + 'hrs)'
                    else:
                        moreless = ' Short(' + str(abs(float(duration_diff))) + 'hrs)'
                    if int(attendancelistin[0].eh) < 10:
                        attendancelistin[0].eh = '0' + str(attendancelistin[0].eh)
                    if int(attendancelistout[0].eh) < 10:
                        attendancelistout[0].eh = '0' + str(attendancelistout[0].eh)
                    if int(attendancelistin[0].em) < 10:
                        attendancelistin[0].em = '0' + str(attendancelistin[0].em)
                    if int(attendancelistout[0].em) < 10:
                        attendancelistout[0].em = '0' + str(attendancelistout[0].em)


                    tmplist.append({qdate: 'InTime-' + str(attendancelistin[0].eh) + ':' + str(
                        attendancelistin[0].em) + 'CLocation-In' + str(attendancelistin[0].ads) +
                        'OutTime-' + str(attendancelistout[0].eh) + ':' + str(attendancelistout[0].em) +
                        'CLocation-Out' + str(attendancelistout[0].ads) +
                        'Duration(' + str(duration) + 'hrs)' + moreless})


                else:

                    tmplist.append({qdate: 'A'})
                    analyticsWorkingdayCount = analyticsWorkingdayCount + 1
            else:

                tmplist.append({qdate: 'A'})
                analyticsWorkingdayCount = analyticsWorkingdayCount + 1
        hlist.append(hduration)
        userlist[str(a.first_name) + ' ' + str(a.last_name) + '(' + str(a.biometric_id) + ')'] = tmplist

    summarydatalist = {}
    nalist = list()
    for dl in datelist1:
        summarydata = Attendance.objects.raw(
            'SELECT id FROM attendance_attendance where user_id in (' + usersIdList[
                                                                        0:-1] + ') and fordate="' + str(
                dl) + '" GROUP BY user_id')
        slist = list()
        if summarydata:
            slist.append(len(summarydata))
            slist.append((len(userlist) - len(summarydata)))
            summarydatalist[dl] = slist
        else:
            summarydatalist[dl] = nalist
    # Analytics
    import matplotlib.pyplot as plt
    import numpy as np
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'Working Days', 'Holidays', 'Week Offs',
    sizes = [analyticsWorkingdayCount, analyticsHolidayCount, analyticsWeekoffCount]
    explode = (0.1, 0, 0)  # only "explode" the 1st slice

    merged_list = [(ulist[i], hlist[i]) for i in range(0, len(ulist))]
    lst = len(merged_list)
    for m in range(0, lst):
        for n in range(0, lst - m - 1):
            # if (merged_list[n][1] > merged_list[n + 1][1]):
            temp = merged_list[n]
            merged_list[n] = merged_list[n + 1]
            merged_list[n + 1] = temp

    ulistfinal = list()
    hlistfinal = list()
    for d in range(0, 7):
        pass
        #ulistfinal.append(merged_list[len(merged_list)-(d+1)][0])
        #hlistfinal.append(merged_list[len(merged_list)-(d+1)][1]/60)
    for c in range(0, 7):
        pass
         #n = float(merged_list[c][1])/60
         #ulistfinal.append(merged_list[c][0])
         #hlistfinal.append(n)

    label = ulistfinal
    no_movies = (hlistfinal)
    logger.info("ttttt")
    logger.info(no_movies)
    index = np.arange(len(label))
    logger.info(index)
    plt.bar(index, no_movies)
    plt.xlabel('Employee', fontsize=5)
    plt.ylabel('No of Hours', fontsize=5)
    plt.xticks(index, label, fontsize=10, rotation=30)
    plt.title('Daily Presence Avg(Top / Least 7)')
    bpath = str(datetime.utcnow() + timedelta(hours=5, minutes=31)) + 'bar'
    imgPathB = '/home/ubuntu/radiant/hrmsrad/content/media/junk/' +bpath + '.png'
    logger.info(imgPathB)
    ana3 = '/media/junk/'+ bpath + '.png'
    plt.savefig(imgPathB)
    plt.close()

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct=make_autopct(sizes),
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    spath = str(datetime.utcnow() + timedelta(hours=5, minutes=31))
    imgPath = '/home/ubuntu/radiant/hrmsrad/content/media/junk/'+spath + '.png'
    logger.info(imgPath)
    ana1 = '/media/junk/' + spath + '.png'
    plt.savefig(imgPath)
    plt.close()

    return render(request, 'attendance/entity_report_ajax.html',
                  {'ana1': ana1, 'ana2': ana1, 'ana3': ana3, 'ana4': ana1, 'userlist': userlist, 'datelist': datelist,
                   'datelist1': datelist1, 'summarylist': summarydatalist, 'totalcandidate': len(usersList)})


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)

    return my_autopct


def ajax_exportdetails(request):
    if request.method == 'GET':
        import pandas as pd
        fromdate = request.GET['fromdate']
        todate = request.GET['todate']
        usertypes = request.GET['utype']
        #selbranch = request.GET['selbranch']
        selshifttime = request.GET['selshifttime']
        selbatch = request.GET['selbatch']
        if (usertypes == 'Employee'):
            tmpEmp = Employee.objects.filter(shifttime_id=int(selshifttime), status=1).order_by('first_name')
        elif (usertypes == 'Student'):
            tmpEmp = Student.objects.filter(batch_id=int(selbatch)).order_by('first_name')
        weekofflist = {}
        minduration = {}

        weekoffs = Shifttime.objects.all()
        for j in weekoffs:
            tmplist1 = list()
            if (j.week_off1):
                tmplist1.append(j.week_off1)
            if (j.week_off2):
                tmplist1.append(j.week_off2)
            if (j.week_off3):
                tmplist1.append(j.week_off3)
            if (j.week_off4):
                tmplist1.append(j.week_off4)
            if (j.week_off5):
                tmplist1.append(j.week_off5)
            weekofflist[j.id] = {}
            weekofflist[j.id]["weekoffs"] = tmplist1
            weekofflist[j.id]["start_time_hh"] = j.start_time_hh
            weekofflist[j.id]["start_time_mm"] = j.start_time_mm
            weekofflist[j.id]["end_time_hh"] = j.end_time_hh
            weekofflist[j.id]["end_time_mm"] = j.end_time_mm
            weekofflist[j.id]["end_time_type"] = j.end_time_type

            minduration[j.id] = j.min_duration_required

        # holidaylist
        holidaylist = list()
        holidays = Holiday.objects.filter(branch_id=1)
        for hd in holidays:
            holidaylist.append(hd.hdate.strftime('%Y-%m-%d'))

        dt = datetime.utcnow() + timedelta(hours=5, minutes=31)
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(os.path.join('/home/ubuntu/radiant/hrmsrad/content/media/junk/', str(dt) + '.xlsx'), engine='xlsxwriter')
        rowList = list()
        columnList = ['BioID', 'Name', 'Department', 'Designation', 'AadharNo', 'DOJ']
        # rowData = ['Project','Department','Designation','BioID','Name','AadharNo','DOJ']
        sdate = datetime.strptime(fromdate, '%Y-%m-%d')  # start date
        edate = datetime.strptime(todate, '%Y-%m-%d')  # end date
        delta = edate - sdate  # as timedelta

        for b in range(delta.days + 1):
            day = sdate + timedelta(days=b)
            qdate = str(day)[0:10]
            columnList.append(qdate)
            columnList.append(' ')
            columnList.append(' ')
        columnList.append('TDays')
        columnList.append('TWDays')
        columnList.append('TP_Days')
        columnList.append('T_WO_H_Days')
        columnList.append('Payable_Days')
        columnList.append('TP_Time_Required (hrs)')
        columnList.append('TP_Time (hrs)')
        columnList.append('Daily_Avg (hrs)')
        columnList.append('Late_Comings_Days')
        columnList.append('Total_Credit (hrs)')
        rowData = list()
        for indx, usr in enumerate(tmpEmp):

            rowList.append(indx + 1)
            tmpRow = list()
            tmpRow = [usr.biometric_id, usr.first_name, usr.department_id, usr.designation_id, usr.aadhar_no,
                      usr.doj]

            workingdays = 0
            tdays = 0
            presentDay = 0
            weekoffHoliday = 0
            userDuration = 0
            totallatecomings = 0
            totallate = 0
            for b in range(delta.days + 1):
                tdays = tdays + 1
                day = sdate + timedelta(days=b)
                qdate = str(day)[0:10]
                if qdate in holidaylist:
                    tmpRow.append('Holiday')
                    tmpRow.append('NA')
                    tmpRow.append('NA')
                    weekoffHoliday = weekoffHoliday + 1
                elif day.weekday() in weekofflist:
                    tmpRow.append('Week Off')
                    tmpRow.append('NA')
                    tmpRow.append('NA')
                    weekoffHoliday = weekoffHoliday + 1
                elif (weekofflist[usr.shifttime_id]["end_time_type"] == 1):
                    logger.info("ttxxtt")
                    logger.info(weekofflist[usr.shifttime_id]["end_time_type"])
                    workingdays = workingdays + 1
                    attendancelist = Attendance.objects.raw(
                        "SELECT id,user_id,fordate,event_hh as eh,event_mm as em,event_ss as es FROM attendance_attendance where fordate='" + qdate + "' and user_id='" + str(
                            usr.user_id) + "' order by event_hh ,event_mm  limit 1")
                    attendancelist1 = Attendance.objects.raw(
                        "SELECT id,user_id,fordate,event_hh as eh,event_mm as em,event_ss as es FROM attendance_attendance where fordate='" + qdate + "' and user_id='" + str(
                            usr.user_id) + "' order by event_hh desc,event_mm desc limit 1")
                    if (len(attendancelist) > 0 and len(attendancelist1) > 0):

                        presentDay = presentDay + 1
                        batchlatetime = str(weekoffs[0].latecoming_hh).zfill(2) + ':' + str(
                            weekoffs[0].latecoming_mm).zfill(2)
                        StartTime = str(attendancelist[0].eh).zfill(2) + ':' +str(attendancelist[0].em).zfill(2)


                        batchStartTime = str(j.start_time_hh).zfill(2) + str(j.start_time_mm).zfill(
                            2)

                        batchEndTime = str(j.end_time_hh).zfill(2) + str(j.end_time_mm).zfill(2)
                        candidateStartTime = str(attendancelist[0].eh).zfill(2) + str(attendancelist[0].em).zfill(
                            2)
                        candidateEndTime = str(attendancelist1[0].eh).zfill(2) + str(attendancelist1[0].em).zfill(
                            2)

                        finalstarthour = int(attendancelist[0].eh)
                        finalstartmin = int(attendancelist[0].em)
                        finalendhour = int(attendancelist1[0].eh)
                        finalendmin = int(attendancelist1[0].em)

                        if (int(candidateStartTime) < int(batchStartTime)):
                            finalstarthour = int(j.start_time_hh)
                            finalstartmin = int(j.start_time_mm)
                        if (int(candidateEndTime) > int(batchEndTime)):
                            finalendhour = int(j.end_time_hh)
                            finalendmin = int(j.end_time_mm)
                         # lateComings Count
                        if StartTime <= batchlatetime:
                            totallate = totallate + 0
                        elif StartTime > batchlatetime:
                            totallate = totallate + 1
                            if totallate > 3:
                               totallatecomings = 30 / ((totallate - 1) * 3)
    

                        finalStartTmp = (finalstarthour * 60 + finalstartmin) / 60
                        finalEndTmp = (finalendhour * 60 + finalendmin) / 60
                        LateComing = totallatecomings * 4
                        proDuration = int(finalEndTmp) - int(finalStartTmp)
                        shortExtra = (proDuration - (minduration[usr.shifttime_id])) / 60
                        userDuration = (userDuration + proDuration + LateComing)
                        tmpRow.append('Present')
                        tmpRow.append(str(attendancelist[0].eh) + ':' + str(attendancelist[0].em) + ':' + str(
                            attendancelist[0].es))
                        tmpRow.append(str(attendancelist1[0].eh) + ':' + str(attendancelist1[0].em) + ':' + str(
                            attendancelist1[0].es))
                    else:
                        tmpRow.append('Absent')
                        tmpRow.append('NA')
                        tmpRow.append('NA')

                else:
                    logger.info("abcd")
                    presentDay = presentDay + 1
                    shift_start = weekoffs[0].start_time_hh - 1
                    shift_end = weekoffs[0].end_time_hh + 5
                    tmpday = sdate + timedelta(days=b + 1)
                    nextqdate = str(tmpday)[0:10]

                    attendancelistin = Attendance.objects.raw(
                        "SELECT id,user_id,fordate,event_hh as eh,event_mm as em,event_ss as es FROM attendance_attendance where fordate='" + qdate + "' and event_hh >=' " + str(
                            shift_start) + "' and   user_id='" + str(
                            usr.user_id) + "' order by event_hh,event_mm limit 1")

                    attendancelistout = Attendance.objects.raw(
                        "SELECT id,user_id,fordate,event_hh as eh,event_mm as em,event_ss as es FROM attendance_attendance where fordate='" + nextqdate + "' and event_hh <' " + str(
                            shift_end) + "' and  user_id='" + str(
                            usr.user_id) + "' order by event_hh desc,event_mm desc limit 1")
                    if (len(attendancelistin) > 0 and len(attendancelistout) > 0):
                        logger.info("tttxxxtttt")
                        finalstarthour = int(attendancelistin[0].eh)
                        finalstartmin = int(attendancelistin[0].em)
                        finalendhour = int(attendancelistout[0].eh)
                        finalendmin = int(attendancelistout[0].em)
                        logger.info(finalstarthour)
                        logger.info(finalstartmin)
                        logger.info(finalendhour)
                        logger.info(finalendmin)

                        finalStartTmp = (finalstarthour * 60 + finalstartmin) / 60
                        finalEndTmp = (finalendhour * 60 + finalendmin) / 60

                        proDuration = int(finalEndTmp) + int(finalStartTmp)
                        shortExtra = (proDuration - (minduration[usr.shifttime_id])) / 60
                        userDuration = (userDuration + proDuration)
                        tmpRow.append('Present')
                        tmpRow.append(str(attendancelistin[0].eh) + ':' + str(attendancelistin[0].em) + ':' + str(
                            attendancelistin[0].es))
                        tmpRow.append(str(attendancelistout[0].eh) + ':' + str(attendancelistout[0].em) + ':' + str(
                            attendancelistout[0].es))

                    else:
                        tmpRow.append('Absent')
                        tmpRow.append('NA')
                        tmpRow.append('NA')
            dailyAvg = 0
            presentDailyAvg = 0
            if presentDay > 0:
                presentDailyAvg = round(userDuration / presentDay, 2)
            tmpRow.append(tdays)
            tmpRow.append(workingdays)
            tmpRow.append(presentDay)
            tmpRow.append(weekoffHoliday)
            tmpRow.append(int(presentDay) + int(weekoffHoliday))
            tmpRow.append((minduration[usr.shifttime_id] * workingdays) / 60)
            tmpRow.append(userDuration)
            tmpRow.append(presentDailyAvg)
            tmpRow.append(totallatecomings)

            tmpRow.append((minduration[usr.shifttime_id] * workingdays) / 60 - userDuration)

            rowData.append(tmpRow)

        tmpIndex = pd.DataFrame(rowData, index=rowList, columns=columnList)
        tmpIndex.to_excel(writer, sheet_name=str(fromdate) + '|To|' + str(todate))

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        file_path = os.path.join('/home/ubuntu/radiant/hrmsrad/content/media/junk/', str(dt) + '.xlsx')

        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                return response
        raise Http404


def ajax_exportsummary(request):
    return render(request, 'attendance/entity_report_ajax.html')


def save(request):
    return render(request, 'attendance/facerecog.html')


# for access of mark attendance
@login_required
@csrf_exempt
def submit(request):
    etype = request.POST.get('event_type')
    lat = request.POST.get('lat')
    lon = request.POST.get('lon')
    data = request.POST.get('imageBase64')
    format, imgstr = data.split(';base64,')
    ext = format.split('/')[-1]
    imgdata = base64.b64decode(imgstr)
    filename = request.user.username + '.' + ext  # I assume you have a way of picking unique filenames
    with open(CONTENT_DIR + '/media/tmppics/' + filename, 'wb') as f:
        f.write(imgdata)

    currentDT = datetime.utcnow() + timedelta(hours=5, minutes=31)
    ehh = currentDT.hour
    emm =currentDT.minute
    ess = currentDT.second
    cdate = currentDT.date()
    #for location
    #api_key = "AIzaSyAoDC05K-AXhYcIk3Op_UMIqXZd1Wh8Ktk"
    locator = Nominatim(user_agent="app")
    location = locator.reverse((lat,lon))
    #location = locator.reverse((28.598810,77.309680))
    address = location.address
    print(address)
   #AWS ACCESS KEY
    access_key_id = 'AKIA6JBPADW4DLWMOJBN'
    secret_access_key = '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'

    #file Uploading..
    local_file =CONTENT_DIR+'/media/tmppics/'+filename
    today = str(datetime.utcnow() + timedelta(hours=5, minutes=31))
    s3_file = "attend_local/"+ request.user.username +"/" + today + os.path.basename(filename)
    print(s3_file)

    KEY_TARGET=os.path.basename(filename)
    Bucket = "attenddencedata"

    logger.info(local_file)
    logger.info(s3_file)
    logger.info(KEY_TARGET)

    def upload_to_aws(local_file, Bucket, s3_file):
        s3 = boto3.client('s3', aws_access_key_id=access_key_id,
                          aws_secret_access_key=secret_access_key)

        try:
            s3.upload_file(local_file, Bucket, s3_file)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False
    uploaded = upload_to_aws(local_file, Bucket, s3_file)
    print(uploaded)

    if uploaded:
       try:
           def compare_faces(bucket, key, bucket_target, key_target, threshold=80, region="eu-west-2"):
               access_key_id = 'AKIA6JBPADW4DLWMOJBN'
               secret_access_key = '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'
               rekognition = boto3.client("rekognition", region, aws_access_key_id=access_key_id,
                                          aws_secret_access_key=secret_access_key)
               response = rekognition.compare_faces(

                   SourceImage={
                       "S3Object": {
                           "Bucket": bucket,
                           "Name": key,
                       }
                   },
                   TargetImage={
                       "S3Object": {
                           "Bucket": bucket_target,
                           "Name": key_target,
                       }
                   },

                   SimilarityThreshold=threshold,
               )
               return response['SourceImageFace'], response['FaceMatches']

           source_face, matches = compare_faces(Bucket, s3_file, Bucket, KEY_TARGET)
           print("Source Face ({Confidence}%)".format(**source_face))
           # one match for each target face
           for match in matches:
               print("Target face ({Confidence}%)".format(**match['Face']))
               print("  Similarity : {}%".format(match['Similarity']))
           if matches:
              tmpAttendance = Attendance.objects.create(
                   user_id=request.user.id,
                   lattitude=lat,
                   longitude=lon,
                   fordate=cdate,
                   event_hh=ehh,
                   event_mm=emm,
                   event_type=etype,
                   event_ss=ess,
                   address=address)

              return JsonResponse({'error':True, 'message':'Face Matched and Uploaded Successfully '})

           else:
               return JsonResponse({'error': False, 'message': 'Face has not Match , Please try again!'})

           return  JsonResponse({'error':True, 'message':'Face Found and Match Successfully '})

       except Exception as e:
              trace_back = traceback.format_exc()
              message = str(e) + " " +str(trace_back)
              logger.info("heyError")
              logger.info(message)
              return JsonResponse({'error': False, 'message': 'Face Not Found , Please try again!'})

    else:
        return JsonResponse({'error': False, 'message': 'Your Image is not upload so Please try Again!'})

    return JsonResponse({'error': True, 'message': 'Successfully captured and Marked Attendance .'})
