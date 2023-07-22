from django.urls import path
from attendee import views
from .views import (
EmployeeListView,EmployeeCreate,EmployeeUpdate,EmployeeDelete,
StudentListView,StudentCreate,StudentUpdate,StudentDelete
)

app_name = 'attendee'

urlpatterns = [
    path('employee/', EmployeeListView.as_view(), name='employee'),
    path('employee/add', EmployeeCreate.as_view(), name='employee_create'),
    path('employee/edit/<int:pk>', EmployeeUpdate.as_view(), name='employee_edit'),
    path('employee/delete/<int:pk>', EmployeeDelete.as_view(), name='employee_delete'),

    path('student/', StudentListView.as_view(), name='student'),
    path('student/add', StudentCreate.as_view(), name='student_create'),
    path('student/edit/<int:pk>', StudentUpdate.as_view(), name='student_edit'),
    path('student/delete/<int:pk>', StudentDelete.as_view(), name='student_delete'),
    path('export_student/', views.export_student, name='export_student'),
    path('export_employee/', views.export_employee, name='export_employee'),
    path('export_holiday/', views.export_holiday, name='export_holiday'),

    path('import-employee/', views.import_employee, name='import_employee'),
    path('import-student/', views.import_student, name='import_student'),
    path('employee/ajax_load_branches', views.load_branches, name='ajax_load_branches'),
    path('employee/ajax_load_employees', views.load_employees, name='ajax_load_employees'),
    path('employee/ajax_branch_employees', views.branch_employees, name='ajax_branch_employees'),
    path('student/ajax_load_branches', views.load_branches, name='ajax_load_branches'),
    path('student/ajax_load_batches', views.load_batches, name='ajax_load_batches'),
    path('student/ajax_branch_batches', views.branch_batches, name='ajax_branch_batches'),

    path('holidaylist/',views.holiday_list, name='holidaylist'),
    path('leavetype/',views.leavetype_list, name='leavetype'),
    path("empattreport/", views.empattreport, name="empattreport"),
    path("empattreportajax/", views.empattreportajax, name="empattreportajax"),
    path("api/createnewuser/", views.createnewuser, name="createnewuser"),
    path("api/addnewattendance/", views.addnewattendance, name="addnewattendance"),
    path("mydetails/", views.mydetails, name="mydetails"),
    path("savepersonaldetails/", views.savepersonaldetails, name="savepersonaldetails"),
    path("savequalificationdetails/", views.savequalificationdetails, name="savequalificationdetails"),
    path("deletequalification/", views.deletequalification, name="deletequalification"),
    path("saveexperiencedetails/", views.saveexperiencedetails, name="saveexperiencedetails"),
    path("deleteexperiencedoc/", views.deleteexperiencedoc, name="deleteexperiencedoc"),
    path("pushmauticform/", views.pushmauticform, name="pushmauticform"),
    path("getCityAjax/", views.getCityAjax, name="getCityAjax"),
    path('img_submit/', views.img_submit, name='img_submit'),
    path('change/', views.change, name='change'),
]
