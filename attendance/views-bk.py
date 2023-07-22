from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from django.views.generic import ListView, UpdateView, DeleteView
from .models import Attendance
from attendee.models import Employee, Student
from datetime import timedelta, datetime
from hierarchy.models import Branch, Batch, Holiday, Shifttime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.decorators import adminaccess_required
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from tablib import Dataset
from django.conf import settings
import os
import csv, logging
from .resources import StudentattendanceResource, EmployeeattendanceResource
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    EmployeeattendanceForm
)
from django.contrib.auth import get_user_model

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
    clist = accessible_branchlist(request)

    if eid:
        employee_list = Employee.objects.filter(pk=eid)
    elif searchString and request.user.is_superuser:
        employee_list = Employee.objects.filter(first_name__icontains=searchString)
    elif request.user.is_superuser:
        employee_list = Employee.objects.filter()
    elif adminaccessfor == 'ce' or adminaccessfor == 'fr':
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
    utype = request.GET['utype']
    branch = request.GET['selbranch']
    fromdate = request.GET['fromdate']
    todate = request.GET['todate']
    batch = request.GET['selbatch']
    employeeid = request.GET['selemployee']

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
        if (((utype == 'Employee') and (int(j.branch_id) == int(branch)) and (j.status) == 1) or (
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

        # if end_time_type ==1:
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
            logger.info(qdate)

            '''attendancelist=Attendance.objects.filter(
                user_id=a.user_id,
                fordate=qdate'
            )'''

            attendancelist = Attendance.objects.raw(
                "SELECT id,user_id,fordate,event_hh as eh,event_mm as em,event_ss as es FROM attendance_attendance where fordate='" + qdate + "' and user_id='" + str(
                    a.user_id) + "' order by event_hh,event_mm limit 1")
            attendancelist1 = Attendance.objects.raw(
                "SELECT id,user_id,fordate,event_hh as eh,event_mm as em,event_ss as es FROM attendance_attendance where fordate='" + qdate + "' and user_id='" + str(
                    a.user_id) + "' order by event_hh desc,event_mm desc limit 1")

            '''shiftentry_start = Shifttime.start_time_hh - 2
            shift_end = Shifttime.end_time_hh + 6
            attendancelist = Attendance.objects.raw(
                "SELECT id,user_id,fordate,event_hh as eh,event_mm as em,event_ss as es FROM attendance_attendance where fordate='" + qdate + "' and event_hh >' " + shiftentry_start + "' and   user_id='" + str(
                    request.user.id) + "' order by event_hh,event_mm limit 1")
            attendancelist1 = Attendance.objects.raw(
                "SELECT id,user_id,fordate,event_hh as eh,event_mm as em,event_ss as es FROM attendance_attendance where fordate='" + qdate + "' and event_hh <' " + shift_end + "' and  user_id='" + str(
                    request.user.id) + "' order by event_hh desc,event_mm desc limit 1")'''

            datelist.append(datetime.strptime(qdate, '%Y-%m-%d').strftime('%d%b`%y'))
            datelist1.append(qdate)

            if qdate in holidaylist:
                analyticsHolidayCount = analyticsHolidayCount + 1
                tmplist.append({qdate: 'H'})
            elif day.weekday() in weekofflist:
                analyticsWeekoffCount = analyticsWeekoffCount + 1
                tmplist.append({qdate: 'WO'})
            elif attendancelist and attendancelist1:
                analyticsWorkingdayCount = analyticsWorkingdayCount + 1
                if Shifttime.end_time_type == 1:
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
                        attendancelist[0].em) + ' OutTime-' + str(attendancelist1[0].eh) + ':' + str(
                        attendancelist1[0].em) + ' Duration(' + str(duration) + 'hrs)' + moreless})
                else:
                    shiftentry_start = Shifttime.start_time_hh -2
                    shift_end = Shifttime.end_time_hh +6
                    shiftstartlist = Attendance.objects.raw(
                        "SELECT id,user_id,fordate,event_hh as eh,event_mm as em,event_ss as es FROM attendance_attendance where fordate='" + qdate + "' and event_hh >' " + shiftentry_start + "' and   user_id='" + str(
                            request.user.id) + "' order by event_hh,event_mm limit 1")
                    shiftendlist = Attendance.objects.raw(
                        "SELECT id,user_id,fordate,event_hh as eh,event_mm as em,event_ss as es FROM attendance_attendance where fordate='" + qdate + "' and event_hh <' " + shift_end + "' and  user_id='" + str(
                            request.user.id) + "' order by event_hh desc,event_mm desc limit 1")
                    duration = 0

                    batchStartTime = str(weekoffs[0].start_time_hh).zfill(2) + str(weekoffs[0].start_time_mm).zfill(2)
                    batchEndTime = str(weekoffs[0].end_time_hh).zfill(2) + str(weekoffs[0].end_time_mm).zfill(2)
                    candidateStartTime = str(shiftstartlist[0].eh).zfill(2) + str(shiftstartlist[0].em).zfill(
                        2)

                    candidateEndTime = str(shiftendlist[0].eh).zfill(2) + str(shiftendlist[0].em).zfill(
                        2)

                    finalstarthour = int(shiftstartlist[0].eh)
                    finalstartmin = int(shiftstartlist[0].em)
                    finalendhour = int(shiftendlist[0].eh)
                    finalendmin = int(shiftendlist[0].em)

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
                    if int(shiftstartlist[0].eh) < 10:
                        shiftstartlist[0].eh = '0' + str(shiftstartlist[0].eh)
                    if int(shiftendlist[0].eh) < 10:
                        shiftendlist[0].eh = '0' + str(shiftendlist[0].eh)
                    if int(shiftstartlist[0].em) < 10:
                        shiftstartlist[0].em = '0' + str(shiftstartlist[0].em)
                    if int(shiftendlist[0].em) < 10:
                        shiftendlist[0].em = '0' + str(shiftendlist[0].em)
                    tmplist.append({qdate: 'InTime-' + str(shiftstartlist[0].eh) + ':' + str(
                        shiftstartlist[0].em) + ' OutTime-' + str(shiftendlist[0].eh) + ':' + str(
                        shiftendlist[0].em) + ' Duration(' + str(duration) + 'hrs)' + moreless})

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
        # ulistfinal.append(merged_list[len(merged_list)-(d+1)][0])
        # hlistfinal.append(merged_list[len(merged_list)-(d+1)][1]/60)
    for c in range(0, 7):
        pass
        # ulistfinal.append(merged_list[c][0])
        # hlistfinal.append(merged_list[c][1]/60)

    label = ulistfinal
    no_movies = hlistfinal
    index = np.arange(len(label))
    plt.bar(index, no_movies)
    plt.xlabel('Employee', fontsize=5)
    plt.ylabel('No of Hours', fontsize=5)
    plt.xticks(index, label, fontsize=10, rotation=30)
    plt.title('Daily Presence Avg(Top / Least 7)')
    bpath = str(datetime.now()) + 'bar'
    imgPathB = os.path.join(settings.JUNK_ROOT, bpath + '.png')
    ana3 = '/media/junk/' + bpath + '.png'
    plt.savefig(imgPathB)
    plt.close()

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct=make_autopct(sizes),
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    spath = str(datetime.now())
    imgPath = os.path.join(settings.JUNK_ROOT, spath + '.png')
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
        selbranch = request.GET['selbranch']
        selbatch = request.GET['selbatch']
        if (usertypes == 'Employee'):
            tmpEmp = Employee.objects.filter(branch_id=int(selbranch), status=1).order_by('first_name')
        elif (usertypes == 'Student'):
            tmpEmp = Student.objects.filter(batch_id=int(selbatch)).order_by('first_name')
        weekofflist = list()
        minduration = 0
        weekoffs = Branch.objects.filter(
            id=int(selbranch)
        )
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
        holidaylist = list()
        holidays = Holiday.objects.filter(branch_id=int(selbranch))
        for hd in holidays:
            holidaylist.append(hd.hdate.strftime('%Y-%m-%d'))

        dt = datetime.now()
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(os.path.join(settings.JUNK_ROOT, str(dt) + '.xlsx'), engine='xlsxwriter')
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
        columnList.append('Total_Credit (hrs)')
        rowData = list()
        for indx, usr in enumerate(tmpEmp):
            rowList.append(indx + 1)
            tmpRow = list()
            tmpRow = [usr.biometric_id, usr.first_name, usr.department.name, usr.designation.name, usr.aadhar_no,
                      usr.doj]

            workingdays = 0
            tdays = 0
            presentDay = 0
            weekoffHoliday = 0
            userDuration = 0
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
                else:
                    workingdays = workingdays + 1
                    attendancelist = Attendance.objects.raw(
                        "SELECT id,user_id,fordate,event_hh as eh,event_mm as em,event_ss as es FROM attendance_attendance where fordate='" + qdate + "' and user_id='" + str(
                            usr.user_id) + "' order by event_hh ,event_mm  limit 1")
                    attendancelist1 = Attendance.objects.raw(
                        "SELECT id,user_id,fordate,event_hh as eh,event_mm as em,event_ss as es FROM attendance_attendance where fordate='" + qdate + "' and user_id='" + str(
                            usr.user_id) + "' order by event_hh desc,event_mm desc limit 1")
                    if (len(attendancelist) > 0 and len(attendancelist1) > 0):
                        presentDay = presentDay + 1
                        batchStartTime = str(weekoffs[0].start_time_hh).zfill(2) + str(weekoffs[0].start_time_mm).zfill(
                            2)
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
                            finalendhour = int(weekoffs[0].end_time_hh)
                            finalendmin = int(weekoffs[0].end_time_mm)

                        finalStartTmp = (finalstarthour * 60 + finalstartmin) / 60
                        finalEndTmp = (finalendhour * 60 + finalendmin) / 60

                        proDuration = int(finalEndTmp) - int(finalStartTmp)
                        shortExtra = (proDuration - (minduration)) / 60
                        userDuration = (userDuration + proDuration)
                        tmpRow.append('Present')
                        tmpRow.append(str(attendancelist[0].eh) + ':' + str(attendancelist[0].em) + ':' + str(
                            attendancelist[0].es))
                        tmpRow.append(str(attendancelist1[0].eh) + ':' + str(attendancelist1[0].em) + ':' + str(
                            attendancelist1[0].es))
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
            tmpRow.append((minduration * workingdays) / 60)
            tmpRow.append(userDuration)
            tmpRow.append(presentDailyAvg)
            tmpRow.append((minduration * workingdays) / 60 - userDuration)

            rowData.append(tmpRow)

        tmpIndex = pd.DataFrame(rowData, index=rowList, columns=columnList)
        tmpIndex.to_excel(writer, sheet_name=str(fromdate) + '|To|' + str(todate))

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        file_path = os.path.join(settings.JUNK_ROOT, str(dt) + '.xlsx')

        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                return response
        raise Http404


def ajax_exportsummary(request):
    return render(request, 'attendance/entity_report_ajax.html')
