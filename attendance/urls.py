from django.urls import path, include
from attendance import views


from .views import (
    EmployeeattendanceListView, EmployeeattendanceUpdate, EmployeeattendanceDelete, export_employeeattendance,
    import_employeeattendance,
    StudentattendanceListView, StudentattendanceUpdate, StudentattendanceDelete, export_studentattendance,
    import_studentattendance, RegularisationListView, RegularisationCreate, RegularisationUpdate, RegularisationDelete,
    MyregularisationListView)

app_name = 'attendance'

#router = routers.DefaultRouter()
#router.register(r'api', views.AttendanceViewSet)


urlpatterns = [
    path('import-employeeattendance/',views.import_employeeattendance,name='import_employeeattendance'),
    path('export-employeeattendance/',views.export_employeeattendance,name='export_employeeattendance'),
    path('import-studentattendance/',views.import_studentattendance,name='import_studentattendance'),
    path('export-studentattendance/',views.export_studentattendance,name='export_studentattendance'),
    path('ajaxlist/',views.AjaxList,name='ajaxlist'),
    path('ajaxupdate/',views.Ajaxupdate,name='ajaxupdate'),
    path('employees/', EmployeeattendanceListView.as_view(), name='employees'),
    path('students/', StudentattendanceListView.as_view(), name='students'),
    path('employees/edit/<int:pk>', EmployeeattendanceUpdate.as_view(), name='employees_edit'),
    path('employees/delete/<int:pk>', EmployeeattendanceDelete.as_view(), name='employees_delete'),
    path('students/edit/<int:pk>', StudentattendanceUpdate.as_view(), name='students_edit'),
    path('students/delete/<int:pk>', StudentattendanceDelete.as_view(), name='students_delete'),
    path('employees/ajax_load_employees', views.load_employees, name='ajax_load_employees'),
    path('attendancereport/', views.attendance_report, name='attendancereport'),
    path('attendancereport/ajax_load_reports', views.load_reports, name='ajax_load_reports'),
    path('ajax_exportdetails/', views.ajax_exportdetails, name='ajax_exportdetails'),
    path('ajax_exportsummary/', views.ajax_exportsummary, name='ajax_exportsummary'),
    path('regularisation/', RegularisationListView.as_view(), name='regularisation'),
    path('myregularisation/', MyregularisationListView.as_view(), name='myregularisation'),
    path('regularisation/add', RegularisationCreate.as_view(), name='regularisation_create'),
    path('regularisation/edit/<int:pk>', RegularisationUpdate.as_view(), name='regularisation_edit'),
    path('regularisation/delete/<int:pk>', RegularisationDelete.as_view(), name='regularisation_delete'),
    path('submit/', views.submit, name='submit'),
    path('save/', views.save, name='save'),



    #path('', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]
