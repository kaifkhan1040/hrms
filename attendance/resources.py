from import_export import fields,resources
from import_export.widgets import ForeignKeyWidget
from .models import Attendance
from accounts.models import User
from attendee.models import Employee,Student
from common.models import Country,State,City,Religion,Category,Bank,Department,Designation
from hierarchy.models import Branch,Batch,Device

class StudentattendanceResource(resources.ModelResource):
    user = fields.Field(
        column_name='Student Email',
        attribute='user',
        widget=ForeignKeyWidget(User, 'email'))
    usersl = fields.Field(
        column_name='Student UniqueID',
        attribute='usersl',
        widget=ForeignKeyWidget(Student, 'user_id'))
    class Meta:
        model = Attendance
        fields = ('id','user','usersl', 'intime_hh','intime_mm', 'outtime_hh', 'outtime_mm','lattitude', 'longitude', 'fordate')

class EmployeeattendanceResource(resources.ModelResource):
    user = fields.Field(
        column_name='Employee Email',
        attribute='user',
        widget=ForeignKeyWidget(User, 'email'))
    employeeslug = fields.Field(
        column_name='Employee UniqueID',
        attribute='employeeslug',
        widget=ForeignKeyWidget(Employee, 'employeeslug'))
    class Meta:
        model = Attendance
        fields = ('id','user','employeeslug', 'intime_hh','intime_mm', 'outtime_hh', 'outtime_mm','lattitude', 'longitude', 'fordate')


