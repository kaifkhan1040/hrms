import base64
import json
from calendar import calendar

import boto3
from botocore.exceptions import NoCredentialsError
from django.db.models import F, Count
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
#from pandas import np
import numpy as np
from .models import Employee, Student, Qualification
from common.models import Country, State, City, Religion, Category, Bank, Department, Designation
from attendance.models import Attendance
from hierarchy.models import Branch, Batch, Device, Holiday, Shifttime, LeaveType
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.decorators import student_required, employee_required, superuser_required, adminaccess_required
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from tablib import Dataset
from django.conf import settings
import os, datetime, requests
import csv, logging
from datetime import date, timedelta, datetime
from .resources import StudentResource, EmployeeResource, MyHolidayResource
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    EmployeeForm, StudentForm
)
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.core import serializers

from app.conf.development.settings import MEDIA_ROOT

from app.conf.development.settings import CONTENT_DIR

User = get_user_model()
logger = logging.getLogger(__name__)


@method_decorator([login_required, adminaccess_required], name='dispatch')
class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    paginate_by = 10  # if pagination is desired
    context_object_name = 'my_employee_list'

    def get_queryset(self):
        try:
            a = self.request.GET.get('employee', )
        except KeyError:
            a = None

        employee_list = accessible_employeelist(self.request, a)
        return employee_list

    def dispatch(self, *args, **kwargs):
        return super(EmployeeListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EmployeeListView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Employee'
        return context


@method_decorator([login_required, adminaccess_required], name='dispatch')
class EmployeeCreate(LoginRequiredMixin, CreateView):
    form_class = EmployeeForm
    model = Employee
    success_url = reverse_lazy('attendee:employee')

    def form_valid(self, form):
        tid = 0
        ceid = form.cleaned_data.get('branch')
        if form.cleaned_data['admin_for'] == 1:
            frdata = Branch.objects.get(pk=ceid.id)
            tid = frdata.organisation_id
        elif form.cleaned_data['admin_for'] == 2:
            tid = ceid.id

        tmpBranch = Branch.objects.filter(pk=ceid.id).select_related()
        for k in tmpBranch:
            tmpOrg = str(k.organisation.name).split(str(" "))
            FS = tmpOrg[0][0:2]
            if (len(tmpOrg) > 1):
                FS = str(tmpOrg[0][0:1]) + (tmpOrg[1][0:1])

                            

        tmpUser = User.objects.create_user(email=form.cleaned_data['email'], is_employee='1',
                                            first_name=form.cleaned_data['first_name'],
                                            password=form.cleaned_data['email'], username=form.cleaned_data['first_name'],
                                            editor_type=form.cleaned_data['admin_for'], editor_typeid=tid)
        # tmpUser.save()
        logger.info("txtt")
        now = datetime.now()
        # now = str(datetime.now())[0:10]
        logger.info(now)
        tm = now.month
        if (now.month < 10):
            tm = '0' + str(now.month)

        form.instance.user_id = tmpUser.id
        logger.info(form.instance.user_id)
        form.instance.employeeslug = FS.upper() + tm + str(now.year)[2:4] + str(tmpUser.id).zfill(5)
        logger.info(form.instance.employeeslug)
        self.object = form.save()

        # for aws uplodation.
        filename = form.instance.user.username + '.png'
        # print(filename)
        access_key_id = 'AKIA6JBPADW4DLWMOJBN'
        secret_access_key = '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'
        fs = MEDIA_ROOT + '/employeepics/' + filename
        # print(fs)
        s3_file = os.path.basename(filename)
        Bucket = "attenddencedata"

        def upload_to_aws(fs, Bucket, s3_file):
            s3 = boto3.client('s3', aws_access_key_id=access_key_id,
                              aws_secret_access_key=secret_access_key)

            try:
                s3.upload_file(fs, Bucket, s3_file)
                print("Upload Successful")
                return True
            except FileNotFoundError:
                print("The file was not found")
                return False
            except NoCredentialsError:
                print("Credentials not available")
                return False

        uploaded = upload_to_aws(fs, Bucket, s3_file)
        print(uploaded)

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(EmployeeCreate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Add Employee'
        return context


@method_decorator([login_required, adminaccess_required], name='dispatch')
class EmployeeUpdate(LoginRequiredMixin, UpdateView):
    form_class = EmployeeForm
    model = Employee
    success_url = reverse_lazy('attendee:employee')

    def form_valid(self, form):
        tid = 0
        ceid = form.cleaned_data.get('branch')
        if form.cleaned_data['admin_for'] == 1:
            frdata = Branch.objects.get(id=ceid.id)
            tid = frdata.organisation_id
        elif form.cleaned_data['admin_for'] == 2:
            tid = ceid

        self.object = form.save()
        User.objects.filter(pk=self.object.user_id).update(editor_type=form.cleaned_data['admin_for'],
                                                           editor_typeid=tid,username=form.cleaned_data['first_name'])
        # tmpUser.save()
        # form.instance.user_id=tmpUser.id
        #for aws uplodation.
        filename = form.instance.user.username + '.png'
        #print(filename)
        access_key_id = 'AKIA6JBPADW4DLWMOJBN'
        secret_access_key = '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'
        fs = MEDIA_ROOT + '/employeepics/' + filename
        #print(fs)
        s3_file = os.path.basename(filename)
        Bucket = "attenddencedata"

        def upload_to_aws(fs, Bucket, s3_file):
            s3 = boto3.client('s3', aws_access_key_id=access_key_id,
                              aws_secret_access_key=secret_access_key)

            try:
                s3.upload_file(fs, Bucket, s3_file)
                print("Upload Successful")
                return True
            except FileNotFoundError:
                print("The file was not found")
                return False
            except NoCredentialsError:
                print("Credentials not available")
                return False

        uploaded = upload_to_aws(fs, Bucket, s3_file)
        print(uploaded)

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(EmployeeUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Update Employee'
        return context


@method_decorator([login_required, adminaccess_required], name='dispatch')
class EmployeeDelete(LoginRequiredMixin, DeleteView):
    model = Employee

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    success_url = reverse_lazy('attendee:employee')


@method_decorator([login_required, adminaccess_required], name='dispatch')
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    paginate_by = 10  # if pagination is desired
    context_object_name = 'my_student_list'

    def get_queryset(self):
        try:
            a = self.request.GET.get('student', )
        except KeyError:
            a = None
        '''if a:
            student_list = Student.objects.filter(
                first_name__icontains=a,
            )
        else:
            student_list = Student.objects.filter()'''
        student_list = accessible_studentlist(self.request, a)
        return student_list

    def dispatch(self, *args, **kwargs):
        return super(StudentListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Student'
        return context


@method_decorator([login_required, adminaccess_required], name='dispatch')
class StudentCreate(LoginRequiredMixin, CreateView):
    form_class = StudentForm
    model = Student
    success_url = reverse_lazy('attendee:student')

    def form_valid(self, form):
        bid = form.cleaned_data.get('branch')
        tmpBranch = Branch.objects.filter(pk=bid.id).select_related()
        for k in tmpBranch:
            tmpOrg = str(k.organisation.name).split(str(" "))
            FS = tmpOrg[0][0:2]
            if (len(tmpOrg) > 1):
                FS = str(tmpOrg[0][0:1]) + (tmpOrg[1][0:1])

        tmpUser = User.objects.create_user(email=form.cleaned_data['email'], is_student='1',
                                           password=form.cleaned_data['email'], username=form.cleaned_data['email'])

        now = datetime.datetime.now()
        tm = now.month
        if (now.month < 10):
            tm = '0' + str(now.month)

        form.instance.user_id = tmpUser.id
        form.instance.studentslug = FS.upper() + tm + str(now.year)[2:4] + str(2).zfill(5)

        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(StudentCreate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Add Student'
        return context


@method_decorator([login_required, adminaccess_required], name='dispatch')
class StudentUpdate(LoginRequiredMixin, UpdateView):
    form_class = StudentForm
    model = Student
    success_url = reverse_lazy('attendee:student')

    def get_context_data(self, **kwargs):
        context = super(StudentUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'RadiantHRMS | Update Student'
        return context


@method_decorator([login_required, adminaccess_required], name='dispatch')
class StudentDelete(LoginRequiredMixin, DeleteView):
    model = Student

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    success_url = reverse_lazy('attendee:student')


@login_required
def export_student(request):
    student_resource = StudentResource()
    dataset = student_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    return response


@login_required
def export_employee(request):
    employee_resource = EmployeeResource()
    dataset = employee_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'
    return response


@login_required
def export_holiday(request):
    myholiday_resource = MyHolidayResource()

    dataset = myholiday_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="myholiday.csv"'
    return response


@login_required
def import_employee(request):
    if request.method == 'POST':
        logger.info("txt")
        employee_resource = EmployeeResource()
        dataset = Dataset()
        logger.info(dataset)
        new_employees = request.FILES['myfile']

        imported_data = dataset.load(new_employees.read().decode('utf-8'), format='csv')
        logger.info(imported_data)
        result = employee_resource.import_data(dataset, dry_run=True, raise_errors=True)  # Test the data import

        if not result.has_errors():
            employee_resource.import_data(dataset, dry_run=False)  # Actually import now
    '''import pandas as pd
    # chunk to write  into csv for import format
    datalist = list()
    tmpEmplist = Employee.objects.filter(status=1)
    loggedInUserData = Employee.objects.filter(user_id=request.user.id)
    for j in tmpEmplist:
        tmpList = list()
        tmpList.append(loggedInUserData[0].branch.name)
        if (loggedInUserData[0].department_id):
            tmpList.append(loggedInUserData[0].department.name)
        else:
            tmpList.append('')
        tmpList.append(j.designation)
        tmpList.append(j.first_name)
        tmpList.append(j.last_name)
        tmpList.append(j.doj)
        tmpList.append(j.email)
        tmpList.append(j.mobile)
        datalist.append(tmpList)
    df1 = pd.DataFrame(datalist,
                       columns=['Branch', 'Department', 'Designation', 'first_name', 'last_name','doj','email','mobile',
                                 'gender', 'status'])
    # df1.reset_index(drop=True, inplace=True)
    df1.to_csv(os.path.join(settings.DATA_ROOT, 'format_employee.csv'), index=False)'''
    DATA_ROOT = settings.DATA_ROOT
    os.rename(os.path.join(DATA_ROOT, 'format_employee.csv'), os.path.join(DATA_ROOT, 'tmp_format_employee.csv'))
    with open(os.path.join(DATA_ROOT, 'tmp_format_employee.csv'), 'r', newline='') as rcsvfile:
        reader = csv.reader(rcsvfile)
        my_list = list(reader)
        with open(os.path.join(DATA_ROOT, 'format_employee.csv'), 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile)      
           
            c4 = Branch.objects.all()           
            
            c5 = Department.objects.all()
            c6 = Designation.objects.all()
            k = 0
            for i in my_list:
            

                # Branch
                if k == 0:
                    i.append('##Branch List##')
                    for d in c4:
                        i.append(d.name)
                # Department
                if k == 0:
                    i.append('##Department List##')
                    for e in c5:
                        i.append(e.name)
                # Designation
                if k == 0:
                    i.append('##Designation List##')
                    for f in c6:
                        i.append(f.name)
                filewriter.writerow(i)
                k = k + 1
    os.remove(os.path.join(DATA_ROOT, 'tmp_format_employee.csv'))
    # chunk to write  into csv for import format

    return render(request, 'attendee/employee_import.html', {'pagetitle': 'RadiantHRMS | Employee Import'})


@login_required
def import_student(request):
    if request.method == 'POST':
        student_resource = StudentResource()
        dataset = Dataset()
        new_students = request.FILES['myfile']

        imported_data = dataset.load(new_students.read().decode('utf-8'), format='csv')
        result = student_resource.import_data(dataset, dry_run=True, raise_errors=True)  # Test the data import

        if not result.has_errors():
            student_resource.import_data(dataset, dry_run=False, raise_errors=True)  # Actually import now
    # chunk to write  into csv for import format
    DATA_ROOT = settings.DATA_ROOT
    os.rename(os.path.join(DATA_ROOT, 'format_student.csv'), os.path.join(DATA_ROOT, 'tmp_format_student.csv'))
    with open(os.path.join(DATA_ROOT, 'tmp_format_student.csv'), 'r', newline='') as rcsvfile:
        reader = csv.reader(rcsvfile)
        my_list = list(reader)
        with open(os.path.join(DATA_ROOT, 'format_student.csv'), 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile)
            sc = Country.objects.all()
            ss = State.objects.all()
            sct = City.objects.all()
            sce = Branch.objects.all()
            sb = Batch.objects.all()
            k = 0
            for i in my_list:
                # Country
                if k == 0:
                    i.append('##CountryList##')
                    for a in sc:
                        i.append(a.name)
                # State
                if k == 1:
                    i.append('##StateList##')
                    for b in ss:
                        i.append(b.name)
                # City
                if k == 2:
                    i.append('##CityList##')
                    for c in sct:
                        i.append(c.name)
                # Branch
                if k == 3:
                    i.append('##BranchList##')
                    for d in sce:
                        i.append(d.name)
                # Batch
                if k == 4:
                    i.append('##BatchList##')
                    for e in sb:
                        i.append(e.name)
                filewriter.writerow(i)
                k = k + 1
    os.remove(os.path.join(DATA_ROOT, 'tmp_format_student.csv'))
    # chunk to write  into csv for import format

    return render(request, 'attendee/student_import.html', {'pagetitle': 'RadiantHRMS | Student Import'})


def load_branches(request):
    branches = accessible_branchlist(request)

    selectedItem = request.GET['sc']
    if not selectedItem:
        selectedItem = 0
    return render(request, 'attendee/city_dropdown_list_options.html',
                  {'branches': branches, 'selectedItem': int(selectedItem)})


def load_employees(request):
    employees = accessible_employeelist(request, '')
    selectedItem = request.GET['sb']
    if not selectedItem:
        selectedItem = 0
    return render(request, 'attendee/employee_dropdown_list_options.html',
                  {'employees': employees, 'selectedItem': int(selectedItem)})


def load_batches(request):
    batches = accessible_batchlist(request)
    selectedItem = request.GET['sb']
    if not selectedItem:
        selectedItem = 0
    return render(request, 'attendee/batch_dropdown_list_options.html',
                  {'batches': batches, 'selectedItem': int(selectedItem)})


def branch_batches(request):
    tmpbatches = accessible_batchlist(request)
    batches = list()
    bof = request.GET['bof']
    for k in tmpbatches:
        if int(k.branch_id) == int(bof):
            batches.append(k)
    return render(request, 'attendee/batch_dropdown_list_options.html', {'batches': batches})


def branch_employees(request):
    tmpemployees = accessible_employeelist(request, '')
    employees = list()
    bof = request.GET['bof']
    for k in tmpemployees:
        if int(k.branch_id) == int(bof):
            employees.append(k)
    return render(request, 'attendee/employee_dropdown_list_options.html', {'employees': employees})


@login_required
def accessible_branchlist(request):
    adminaccessfor = request.session['adminfor']
    adminaccessforId = request.session['adminforId']

    if request.user.is_superuser:
        branch_list = Branch.objects.filter().select_related()
    elif adminaccessfor == 'ce':
        branch_list = Branch.objects.filter(pk=adminaccessforId).select_related()
        logger.info(branch_list)
    elif adminaccessfor == 'fr':
        branch_list = Branch.objects.filter(organisation_id=adminaccessforId).select_related()
        logger.info(branch_list)
    elif request.user.is_employee:
        branch_list = Branch.objects.filter().select_related()
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
def accessible_employeelist(request, searchString):
    adminaccessfor = request.session['adminfor']
    adminaccessforId = request.session['adminforId']
    clist = accessible_branchlist(request)
    if searchString and request.user.is_superuser:
        employee_list = Employee.objects.filter(first_name__icontains=searchString)
    elif request.user.is_superuser:
        employee_list = Employee.objects.filter()
    elif adminaccessfor == 'ce' or adminaccessfor == 'fr':
        

        if searchString:
            employee_list = Employee.objects.filter(branch__in=clist, first_name__icontains=searchString)
        else:
            employee_list = Employee.objects.filter(branch__in=clist)
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
        if searchString:
            student_list = Student.objects.filter(branch__in=clist, first_name__icontains=searchString)
        else:
            student_list = Student.objects.filter(branch__in=clist)
    return student_list


@login_required
def holiday_list(request):
    if request.user.is_employee:
        tmpbranches = Employee.objects.filter(user_id=request.user.id)
    elif request.user.is_student:
        tmpbranches = Student.objects.filter(user_id=request.user.id)
    clist = list()
    for c in tmpbranches:
        clist.append(c.branch_id)
    holiday_list = Holiday.objects.filter(branch__in=clist)

    return render(request, 'attendee/holidays.html',
                  {'pagetitle': 'RadiantHRMS | Holiday List', 'holiday_list': holiday_list})


@login_required
def leavetype_list(request):
    if request.user.is_employee:
        tmpbranches = Employee.objects.filter(user_id=request.user.id)
    clist = list()
    for c in tmpbranches:
        clist.append(c.branch_id)
    leavetype_list = LeaveType.objects.filter(branch__in=clist)

    return render(request, 'attendee/leavetype.html',
                  {'pagetitle': 'RadiantHRMS | LeaaveType List', 'leavetype_list': leavetype_list})


@csrf_exempt
def adduser(request):
    if request.method == 'POST':
        branchId = int(request.POST.get('forbranch'))
        userType = int(request.POST.get('userType'))
        userName = str(request.POST.get('userName'))
        biouserId = int(request.POST.get('biouserId'))
        existing = False
        if userType == 1:
            is_employee = 1
            existing = Employee.objects.filter(
                branch_id=branchId,
                biometric_id=biouserId)
        elif userType == 2:
            is_employee = 0
            existing = Student.objects.filter(
                branch_id=branchId,
                biometric_id=biouserId)

        if (existing and len(existing) > 0):
            response = 'Already Exist!!!'
        else:
            tmpUser = User.objects.create_user(email=str(userName).lower() + str(biouserId) + '@radiantinfonet.com',
                                               is_employee=is_employee,
                                               password=str(userName).lower() + str(biouserId),
                                               username=str(userName).lower() + str(biouserId) + '@radiantinfonet.com',
                                               editor_type=0, editor_typeid=0)
            if (tmpUser.id and userType == 1):
                tmpUsrType = Employee.objects.create(
                    doj=datetime.now(),
                    first_name=userName,
                    email=str(userName).lower() + str(biouserId) + '@radiantinfonet.com',
                    biometric_id=biouserId,
                    branch_id=1,
                    gender=1,
                    marital_status=1,
                    status=1,
                    user_id=tmpUser.id)
            elif (tmpUser.id and userType == 2):
                tmpUsrType = Student.objects.create(
                    first_name=userName,
                    email=str(userName).lower() + str(biouserId) + '@radiantinfonet.com',
                    biometric_id=biouserId,
                    branch_id=1,
                    gender=1,
                    status=1,
                    user_id=tmpUser.id)

            response = tmpUsrType.id

        data = {"results": response}
        return JsonResponse(data)


@csrf_exempt
def empattreport(request):
    return render(request, 'attendee/empattreport.html', {})


@csrf_exempt
def empattreportajax(request):
    formonth = int(request.POST.get('formonth'))
    foryear = int(request.POST.get('foryear'))
    lastdate = 30
    no_data = False
    if (int(formonth) == 1 or int(formonth) == 3 or int(formonth) == 5 or int(formonth) == 7 or int(
            formonth) == 8 or int(formonth) == 10 or int(formonth) == 12):
        lastdate = 31
    elif (int(formonth) == 2):
        lastdate = 28
        if (foryear % 100) == 0:
            if (foryear % 400) == 0:
                lastdate = 29
        elif (foryear % 4) == 0:
            lastdate = 29

    start = str(foryear) + '-' + str(formonth) + '-01'
    end = str(foryear) + '-' + str(formonth) + '-' + str(lastdate)
    sdate = datetime.strptime(start, '%Y-%m-%d')  # start date
    edate = datetime.strptime(end, '%Y-%m-%d')  # end date
    for_month = sdate.month
    for_year = sdate.year

    # weekofflist
    if request.user.is_student:
        a = Student.objects.filter(user_id=request.user.id)
        weekoffs = Batch.objects.filter(
            id=a[0].batch_id
        )
    elif request.user.is_employee:
        a = Employee.objects.filter(user_id=request.user.id)
        weekoffs = Shifttime.objects.filter(
            id=a[0].shifttime_id
        )
    weekofflist = list()
    holidaylist = list()
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
    holidays = Holiday.objects.filter(branch_id=a[0].branch_id)
    for hd in holidays:
        holidaylist.append(hd.hdate.strftime('%Y-%m-%d'))

    delta = edate - sdate  # as timedelta

    addattendancedata = {}
    totallatecomings = 0
    totallate = 0
    dailyavg = 0
    totalworkingdays = 0
    totalweekoffs = 0
    totalminutesworked = 0
    totalabsent = 0
    totalholidays = 0
    totalpresent = 0
    totalshortadditional = 0
    batchStartTime = str(weekoffs[0].start_time_hh).zfill(2) + str(weekoffs[0].start_time_mm).zfill(2)
    batchlatetime = str(weekoffs[0].latecoming_hh).zfill(2) +':'+ str(weekoffs[0].latecoming_mm).zfill(2)
    logger.info(batchStartTime)
    for b in range(delta.days + 1):

        day = sdate + timedelta(days=b)
        qdate = str(day)[0:10]

        currdate = str(datetime.now())[0:10]
        # nextday = datetime.now() + timedelta(days=1)
        todaydate = datetime.strptime(currdate, '%Y-%m-%d')
        indexdate = datetime.strptime(qdate, '%Y-%m-%d')

        if (request.user.employee.doj is None or request.user.employee.doj == ""):
            joiningdate = datetime.strptime('2019-01-01', '%Y-%m-%d')
        else:
            # joiningdate=datetime.strptime(a[0].doj, '%d-%m-%Y').strftime('%Y-%m-%d')
            # joiningdate=datetime.strptime('2019-01-01','%Y-%m-%d')
            joiningdate = datetime.strptime(a[0].doj, '%Y-%m-%d')

        joining_month = joiningdate.month
        joining_year = joiningdate.year

        if (len(a[0].doj) == 10):
            joiningdate = datetime.strptime(a[0].doj, '%Y-%m-%d')

        addattendancedata[qdate] = {}
        addattendancedata[qdate]['Date'] = datetime.strptime(qdate, '%Y-%m-%d').strftime('%d-%B-%Y')

        attendancelist = Attendance.objects.raw(
            "SELECT id,user_id,fordate,address as ads, event_hh as eh,event_mm as em,event_ss as es FROM attendance_attendance where fordate='" + qdate + "' and user_id='" + str(
                request.user.id) + "' order by event_hh,event_mm limit 1")
        logger.info(attendancelist)
        attendancelist1 = Attendance.objects.raw(
            "SELECT id,user_id,fordate,address as ads ,event_hh as eh,event_mm as em,event_ss as es FROM attendance_attendance where fordate='" + qdate + "' and user_id='" + str(
                request.user.id) + "' order by event_hh desc,event_mm desc limit 1")

        addattendancedata[qdate]['in'] = 'NA'
        addattendancedata[qdate]['out'] = 'NA'
        # if(len(attendancelist)>0):
        #     addattendancedata[qdate]['in']=str(attendancelist[0].event_hh)+' : '+str(attendancelist[0].event_mm)
        #     addattendancedata[qdate]['out'] = str(attendancelist1[0].event_hh) +' : '+ str(attendancelist1[0].event_mm)
        addattendancedata[qdate]['in'] = 'NA'
        addattendancedata[qdate]['out'] = 'NA'
        addattendancedata[qdate]['minutes worked'] = 'NA'
        addattendancedata[qdate]['short_additional'] = 'NA'
        addattendancedata[qdate]['on time'] = 'NA'
        addattendancedata[qdate]['Current Location(punch-In)'] = 'NA'
        addattendancedata[qdate]['Current Location(punch-Out)'] = 'NA'


        if indexdate > todaydate or joiningdate > indexdate:
            pass

        elif qdate in holidaylist:
            addattendancedata[qdate]['in'] = 'Holiday'
            addattendancedata[qdate]['out'] = 'Holiday'
            totalholidays = totalholidays + 1
        elif day.weekday() in weekofflist:
            addattendancedata[qdate]['in'] = 'WeekOff'
            addattendancedata[qdate]['out'] = 'WeekOff'
            totalweekoffs = totalweekoffs + 1

        elif (len(attendancelist) > 0 and weekoffs[0].end_time_type == 1):
            logger.info("sweety")
            addattendancedata[qdate]['Current Location(punch-In)'] = str(attendancelist[0].address)
            logger.info(addattendancedata[qdate]['Current Location(punch-In)'])
            totalpresent = totalpresent + 1
            totalworkingdays = totalworkingdays + 1
            addattendancedata[qdate]['in'] = str(attendancelist[0].event_hh) + ' : ' + str(attendancelist[0].event_mm)
            tmpintime = int(attendancelist[0].event_hh * 60 + attendancelist[0].event_mm)
            tmpintime1 = str(attendancelist[0].event_hh ) +':' + str( attendancelist[0].event_mm)

            if tmpintime <= int(batchStartTime):
                addattendancedata[qdate]['on time'] = 'Yes'
            elif tmpintime > int(batchStartTime):
                addattendancedata[qdate]['on time'] = 'No'
                totallate = totallate + 1
                if totallate > 3:
                   totallatecomings = totallatecomings + 1

            #if indexdate == todaydate:
            addattendancedata[qdate]['out'] = str(attendancelist1[0].event_hh) + ' : ' + str(
                attendancelist1[0].event_mm)
            logger.info(addattendancedata[qdate]['out'])
            addattendancedata[qdate]['Current Location(punch-Out)'] = str(attendancelist1[0].ads)
            logger.info(addattendancedata[qdate]['Current Location(punch-Out)'])

            tmpintime = int(attendancelist[0].event_hh * 60 + attendancelist[0].event_mm)
            tmpouttime = int(attendancelist1[0].event_hh * 60 + attendancelist1[0].event_mm)
            addattendancedata[qdate]['minutes worked'] = tmpouttime - tmpintime
            totalminutesworked = totalminutesworked + (tmpouttime - tmpintime)
            addattendancedata[qdate]['short_additional'] = '{0:+} minutes'.format(
                (tmpouttime - tmpintime) - minduration)
            totalshortadditional = totalshortadditional + ((tmpouttime - tmpintime) - minduration)

        elif (len(attendancelist) > 0 and weekoffs[0].end_time_type == 2):
            shift_start = weekoffs[0].start_time_hh - 1
            shift_end = weekoffs[0].end_time_hh + 5
            tmpday = sdate + timedelta(days=b + 1)
            nextqdate = str(tmpday)[0:10]

            attendancelistin = Attendance.objects.raw(
                "SELECT id,user_id,fordate,address as ads,event_hh as eh,event_mm as em,event_ss as es FROM attendance_attendance where fordate='" + qdate + "' and event_hh >=' " + str(
                    shift_start) + "' and   user_id='" + str(
                    request.user.id) + "' order by event_hh,event_mm limit 1")

            attendancelistout = Attendance.objects.raw(
                "SELECT id,user_id,fordate,address as ads,event_hh as eh,event_mm as em,event_ss as es FROM attendance_attendance where fordate='" + nextqdate + "' and event_hh <' " + str(
                    shift_end) + "' and  user_id='" + str(
                    request.user.id) + "' order by event_hh desc,event_mm desc limit 1")

            totalpresent = totalpresent + 1
            totalworkingdays = totalworkingdays + 1
            if attendancelistin:
                addattendancedata[qdate]['in'] = str(attendancelistin[0].event_hh) + ' : ' + str(
                    attendancelistin[0].event_mm)
                tmpintime = int(attendancelistin[0].event_hh * 60 + attendancelistin[0].event_mm)

            if tmpintime <= int(batchStartTime):
                addattendancedata[qdate]['on time'] = 'Yes'
            elif tmpintime > int(batchStartTime):
                addattendancedata[qdate]['on time'] = 'No'
                totallate = totallate + 1
                if totallate > 3:
                    totallatecomings = totallatecomings + 1
            

            #if indexdate != todaydate:
            if attendancelistout and attendancelistin:
                addattendancedata[qdate]['out'] = str(attendancelistout[0].event_hh) + ' : ' + str(
                    attendancelistout[0].event_mm)
                tmpintime = int(1440 - (attendancelistin[0].event_hh * 60 + attendancelistin[0].event_mm))

                tmpouttime = int(attendancelistout[0].event_hh * 60 + attendancelistout[0].event_mm)

                addattendancedata[qdate]['minutes worked'] = tmpouttime + tmpintime
                totalminutesworked = totalminutesworked + (tmpouttime + tmpintime)
                addattendancedata[qdate]['short_additional'] = '{0:+} minutes'.format(
                    (tmpouttime + tmpintime) - minduration)
                totalshortadditional = totalshortadditional + ((tmpouttime + tmpintime) - minduration)

        else:
            # logger.info("text2")

            totalabsent = totalabsent + 1
            addattendancedata[qdate]['in'] = 'A'
            addattendancedata[qdate]['out'] = 'A'
            addattendancedata[qdate]['minutes worked'] = 'NA'
            addattendancedata[qdate]['short_additional'] = 'NA'
            addattendancedata[qdate]['on time'] = 'NA'
            addattendancedata[qdate]['Current Location(punch-In)'] = 'NA'
            addattendancedata[qdate]['Current Location(punch-Out)'] = 'NA'
            totalworkingdays = totalworkingdays + 1

    dailyavg = 0
    if (totalpresent):  # bypass zero value
        tmpdailyavg = totalminutesworked / totalpresent
        dailyavg = "{0:.2f}".format(tmpdailyavg)

    if (joining_year < for_year):
        no_data = False
    elif (joining_year == for_year):
        if (joining_month <= for_month):
            no_data = False
        else:
            no_data = True
    else:
        no_data = True

    return render(request, 'attendee/empattreportajax.html',
                  {'usrAttendance': addattendancedata,'totallatecomings': totallatecomings,'dailyavg': dailyavg,
                   'totalworkingdays': totalworkingdays, 'totalabsent': totalabsent, 'totalpresent': totalpresent,
                   'totalweekoffs': totalweekoffs,
                   'totalshortadditional': '{0:+}'.format(totalshortadditional, 'totalholidays'),
                   'totalholidays': totalholidays, 'joining_month': joining_month, 'joining_year': joining_year,
                   'for_month': for_month, 'for_year': for_year, 'no_data': no_data})



@csrf_exempt
def createnewuser(request):
    try:
        import json
        logger.info(request)
        branchID = str(request.POST.get('branchid')) 
        secretkey = str(request.POST.get('secretkey'))
        userlist = request.POST.get('userdata')        
        jdata = json.loads(userlist)
       
        if (secretkey + str(settings.CLIENT_SALT) == settings.CLIENT_KEY + settings.CLIENT_SALT):
            for d in jdata:
                username = str(d[0])               
                bioid = int(d[1])                
                chkexistinguser = Employee.objects.filter(biometric_id=bioid, branch_id=branchID)
               
                if (len(chkexistinguser) == 0):
                    logger.info('created')
                    tmpnewUser = User.objects.create_user(email=str(username).lower() + '@radiantinfonet.com',
                                                          is_employee='1',
                                                          password=bioid,
                                                          username=str(username).lower() + str(bioid),
                                                          editor_type=0, editor_typeid=0)
                    tmpEmp = Employee.objects.create(
                        email=str(username).lower() + '@radiantinfonet.com',
                        first_name=str(username),
                        biometric_id=bioid,
                        doj=str(datetime.now())[0:10],
                        branch_id=1,
                        department_id=1,
                        designation_id=2,
                        gender=1,
                        marital_status=1,
                        status=1,
                        user_id=tmpnewUser.id,
                    )
            response = 1
        else:
            response = 2
    except IndexError:
        response = 0
    return HttpResponse(response)


@csrf_exempt
def addnewattendance(request):
    if request.method == 'POST':
        import json
        branchId = str(request.POST.get('branchid'))
        secretkey = str(request.POST.get('secretkey'))
        lattitude = str(request.POST.get('lattitude'))
        longitude = str(request.POST.get('longitude'))
        logger.info(lattitude)
        attendanceslist = str(request.POST.get('attendanceslist'))
        tmpattendanceslist = json.loads(attendanceslist)
        logger.info(tmpattendanceslist)
        if (secretkey + str(settings.CLIENT_SALT) == settings.CLIENT_KEY + settings.CLIENT_SALT):
            for j in tmpattendanceslist:
                tmpj = str(j).split(':')
                bioid = tmpj[1].strip()
                tmparr = tmpj[2].split(' ')
                fordate = tmparr[1]
                hh = tmparr[2]
                mm = tmpj[3]
                tmparr1 = tmpj[4].split(' ')
                ss = tmparr1[0]
                ptype = tmparr1[1][1:2]
                existing = Employee.objects.filter(
                    branch_id=branchId,
                    biometric_id=bioid)
                if len(existing) == 0:
                    existing = Student.objects.filter(
                        branch_id=branchId,
                        biometric_id=bioid)
                if len(existing) > 0:
                    userId = existing[0].user_id
                    tmpAttendance = Attendance.objects.create(
                        user_id=userId,
                        lattitude=lattitude,
                        longitude=longitude,
                        fordate=fordate,
                        event_hh=hh,
                        event_mm=mm,
                        event_type=ptype,
                        event_ss=ss)
        data = {"results": 1}
        return JsonResponse(data)


@login_required
@csrf_exempt
def mydetails(request):
    tmpUsr = User.objects.filter(id=request.user.id)
    userDetails = 0
    logger.info("user")
    logger.info((userDetails))
    if tmpUsr[0].is_employee == 1:
        userDetails = Employee.objects.filter(user_id=request.user.id)
    elif tmpUsr[0].is_student == 1:
        userDetails = Student.objects.filter(user_id=request.user.id)

    countrylist = Country.objects.filter(status=1)
    statelist = State.objects.filter(status=1)
    citylist = City.objects.filter(status=1)

    banklist = Bank.objects.filter(status=1)
    categorylist = Category.objects.filter(status=1)
    religionlist = Religion.objects.filter(status=1)
    experience = userDetails[0].experience
   
    qualification_documents = Qualification.objects.filter(user_id=request.user.id)
    context = {}
    context['loop_times'] = range(0, 41)
    DATA_ROOT = settings.DATA_ROOT
    path = DATA_ROOT + "/experience/" + str(request.user.id) + "/"
    user_id = str(request.user.id) + "/"
    # logger.info(path)
    files = []
    # userdata = { "data":[]}
    user_doc = {}
    for r, d, f in os.walk(path):
        for file in f:
            doc_name = file.split('_')[1]
            doc_key = file.split(user_id)[0]
            user_doc[str(doc_key)] = str(doc_name)

    if experience is None:
        experience = 0

    return render(request, 'attendee/mydetails.html', {
        'userDetails': userDetails[0],
        'countrylist': countrylist,
        'statelist': statelist,
        'citylist': citylist,
        'banklist': banklist,
        'categorylist': categorylist,
        'religionlist': religionlist,
        'qualification_documents': qualification_documents,
        'context': context,
        'userdata': user_doc,
        'userId': str(request.user.id),
        'experience': int(experience)
    })





@login_required
@csrf_exempt
def mydetails1(request):
    tmpUsr = User.objects.filter(id=request.user.id)
    userDetails = 0
    logger.info("user")
    logger.info((userDetails))
    if tmpUsr[0].is_employee == 1:
        userDetails = Employee.objects.filter(user_id=request.user.id)
    elif tmpUsr[0].is_student == 1:
        userDetails = Student.objects.filter(user_id=request.user.id)

    countrylist = Country.objects.filter(status=1)
    statelist = State.objects.filter(status=1)
    citylist = City.objects.filter(status=1)

    banklist = Bank.objects.filter(status=1)
    categorylist = Category.objects.filter(status=1)
    religionlist = Religion.objects.filter(status=1)
    experience = userDetails[0].experience
    qualification_documents = Qualification.objects.filter(user_id=request.user.id)
    context = {}
    context['loop_times'] = range(0, 41)
    DATA_ROOT = settings.DATA_ROOT
    path = DATA_ROOT + "/experience/" + str(request.user.id) + "/"
    user_id = str(request.user.id) + "/"
    # logger.info(path)
    files = []
    # userdata = { "data":[]}
    user_doc = {}
    for r, d, f in os.walk(path):
        for file in f:
            doc_name = file.split('_')[1]
            doc_key = file.split(user_id)[0]
            user_doc[str(doc_key)] = str(doc_name)

    if experience is None:
        experience = 0

    return render(request, 'attendee/mydetails.html', {
        'userDetails': userDetails[0],
        'countrylist': countrylist,
        'statelist': statelist,
        'citylist': citylist,
        'banklist': banklist,
        'categorylist': categorylist,
        'religionlist': religionlist,
        'qualification_documents': qualification_documents,
        'context': context,
        'userdata': user_doc,
        'userId': str(request.user.id),
        'experience': int(experience)
    })


@login_required
@csrf_exempt
def deleteexperiencedoc(request):
    if request.method == 'POST':
        import json
        user_id = request.POST.get('user_id')
        img = request.POST.get('img')
        experience = request.POST.get('experience')
        logger.info(user_id, img)
        DATA_ROOT = settings.DATA_ROOT

        if os.path.isfile(DATA_ROOT + '/experience/' + str(user_id) + '/' + str(img)):
            os.remove(DATA_ROOT + '/experience/' + str(user_id) + '/' + str(img))
        data = json.dumps({
            'status': 200,
        })
    return HttpResponse(data, content_type='application/json')


@login_required
@csrf_exempt
def savepersonaldetails(request):
    if request.method == 'POST':
        import json
        posteddata = json.loads(request.POST.get('formdata'))
        old_user = User.objects.get(pk=request.user.id)

        if (old_user.is_employee):
            usertype = Employee.objects.get(user_id=request.user.id)
        elif (old_user.is_student):
            usertype = Student.objects.get(user_id=request.user.id)
        for key, value in posteddata.items():
            setattr(usertype, key, value)
        usertype.save()
    return render(request, 'attendee/mydetails.html', {'': ''})


@login_required
@csrf_exempt
def savequalificationdetails(request):
    if request.method == 'POST':
        import json
        doc = request.FILES['qualification_doc']
        document_of = request.POST.get('qualification_type')
        description = request.POST.get('qualification_desc')
        user_id = request.user.id

        image_types = ['image/png', 'image/jpg', 'image/jpeg', 'image/pjpeg', 'image/gif', 'application/pdf']
        if doc.content_type not in image_types:
            data = json.dumps({
                'status': 405,
                'error': 'Bad image format.'
            })
            return HttpResponse(data, content_type="application/json", status=405)

        newdatetime = datetime.now()
        datetime_str = newdatetime.strftime("%Y-%m-%d-%H-%M-%S")
        DATA_ROOT = settings.DATA_ROOT
        doc_name = str(datetime_str) + '_' + str(user_id) + '_' + doc.name
        fs = FileSystemStorage(location=DATA_ROOT + '/qualification')
        filename = fs.save(doc_name, doc)
        user = User.objects.get(id=user_id)
        add_qualifications = Qualification.objects.create(document_of=document_of, description=description,
                                                          document=doc_name, user_id=user)
        data = json.dumps({
            'status': 200,
            'link': doc_name,
            'name': doc.name,
            'doc_of': document_of,
            'doc_desc': description,
            'token': add_qualifications.id
        })
    return HttpResponse(data, content_type='application/json')


@login_required
@csrf_exempt
def deletequalification(request):
    if request.method == 'POST':
        import json
        qual_id = request.POST.get('qual_id')
        qualification_data = Qualification.objects.get(id=qual_id)
        doc_of = qualification_data.document_of
        DATA_ROOT = settings.DATA_ROOT
        # logger.info(qualification_data.document)
        if qualification_data is not None:
            if os.path.isfile(DATA_ROOT + '/qualification/' + str(qualification_data.document)):
                os.remove(DATA_ROOT + '/qualification/' + str(qualification_data.document))

        Qualification.objects.filter(id=qual_id).delete()
        data = json.dumps({
            'status': 200,
            'doc_of': doc_of
        })
    return HttpResponse(data, content_type='application/json')


@login_required
@csrf_exempt
def saveexperiencedetails(request):
    if request.method == 'POST':
        import json
        uploaded_files = request.FILES.getlist('file')
        experience_data = request.POST.get('experience')
        user_id = request.user.id
        doc_dict = {}

        for k in uploaded_files:
            newdatetime = datetime.now()
            datetime_str = newdatetime.strftime("%Y-%m-%d-%H-%M-%S")
            DATA_ROOT = settings.DATA_ROOT
            doc_name = str(datetime_str) + '-' + str(user_id) + '_' + k.name
            fs = FileSystemStorage(location=DATA_ROOT + '/experience/' + str(user_id))
            filename = fs.save(doc_name, k)
            doc_dict[doc_name] = k.name

        usertype = Employee.objects.get(user_id=user_id)
        usertype.experience = experience_data
        usertype.save()
        data = json.dumps({
            'status': 200,
            'doc': doc_dict,
            'user_id': user_id
            # 'token':add_qualifications.id
        })

    return HttpResponse(data, content_type='application/json')


@login_required
@csrf_exempt
def pushmauticform(request):
    import json, requests
    employee_list = Employee.objects.filter(branch_id=1)
    formid = str(5)
    for k in employee_list:
        email = k.email
        fullname = str(k.first_name) + ' ' + str(k.last_name)  # str(request.POST.get('email'))
        url = 'https://www.radiantinfonet.com/pushmautic.php?formId=' + formid + '&email=' + email + '&name=' + fullname
        r = requests.post(url, '')
        data = {"results": r.text}
    return JsonResponse(data)


@csrf_exempt
def getCityAjax(request):
    if request.method == 'POST':
        import json
        state_id = request.POST.get('state_id')
        citylist = City.objects.filter(state_id=state_id)
        city_list = serializers.serialize('json', citylist)
        # logger.info(citylist)

    return JsonResponse({'data': city_list})


'''@csrf_exempt
def deactivateuser(request):
    data = Employee.objects.all()
    tmpdate = datetime.now() - timedelta(days=60)
    res = {}
    for k in data:
        data.update({'data': data, 'tmpdate': tmpdate})
    return JsonResponse(res)'''


@csrf_exempt
def get_employee(request):
    emp = Employee.objects.filter(branch_id=1)

    data = {}
    for k in emp:
        attendance = Attendance.objects.filter(fordate__gte=datetime.now() - timedelta(days=30),
                                               user_id=k.user_id).values()

        if not attendance:
            # update query for user
            tmpemp = Employee.objects.get(user_id=k.user_id)
            tmpemp.status = '0'
            tmpemp.save()
            # logger.info(k.user_id)
    return JsonResponse(data, safe=False)


'''@csrf_exempt
def get_attendance(request):
    emp = Employee.objects.filter(branch_id=1)

    data = {}
    for k in emp:
        attendance = Attendance.objects.filter(fordate__gte=datetime.now() - timedelta(days=30),
                                               user_id=k.user_id).values()

        if not attendance:
            # update query for user
            tmpusr = User.objects.get(pk=k.user_id)
            tmpusr.is_active = '0'
            tmpusr.save()
            # logger.info(k.user_id)
    return JsonResponse(data, safe=False)'''

def change(request):
    return render(request, 'attendee/change_prof.html')


# for access of mark attendance
@login_required
@csrf_exempt
def img_submit(request):
    data = request.POST.get('imageBase64')
    format, imgstr = data.split(';base64,')
    ext = format.split('/')[-1]
    imgdata = base64.b64decode(imgstr)
    filename = '/employeepics/' + request.user.username + '.' + ext  # I assume you have a way of picking unique filenames
    with open(CONTENT_DIR + '/media'+ filename, 'wb') as f:
        f.write(imgdata)


    tmpEmployee = Employee.objects.filter(user_id=request.user.id).update(profile=filename)

    access_key_id = 'AKIA6JBPADW4DLWMOJBN'
    secret_access_key = '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'

    #file Uploading..
    fs = MEDIA_ROOT + filename
    #print(fs)
    s3_file = os.path.basename(filename)
    #print(s3_file)
    Bucket = "attenddencedata"

    def upload_to_aws(fs, Bucket, s3_file):
        s3 = boto3.client('s3', aws_access_key_id=access_key_id,
                          aws_secret_access_key=secret_access_key)

        try:
            s3.upload_file(fs, Bucket, s3_file)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False

    uploaded = upload_to_aws(fs, Bucket, s3_file)
    print(uploaded)
    return JsonResponse({'error': True, 'message': 'Successfully captured Your Image .'})



