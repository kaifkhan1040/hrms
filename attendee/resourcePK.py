from import_export import fields,resources
from import_export.widgets import ForeignKeyWidget
from .models import Student,Employee
from common.models import Country,State,City,Religion,Category,Bank,Department,Designation
from hierarchy.models import Branch,Batch,Device,Holiday,Shifttime

class StudentResource(resources.ModelResource):
    country = fields.Field(
        column_name='Country',
        attribute='country',
        widget=ForeignKeyWidget(Country, 'name'))
    state = fields.Field(
        column_name='State',
        attribute='state',
        widget=ForeignKeyWidget(State, 'name'))
    city = fields.Field(
        column_name='City',
        attribute='city',
        widget=ForeignKeyWidget(City, 'name'))
    branch = fields.Field(
        column_name='Branch',
        attribute='branch',
        widget=ForeignKeyWidget(Branch, 'name'))
    batch = fields.Field(
        column_name='Batch',
        attribute='batch',
        widget=ForeignKeyWidget(Batch, 'name'))
    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name','studentslug', 'gender', 'dob', 'email', 'mobile', 'qualification', 'address1', 'address2', 'pincode', 'aadhar_no', 'profilepic', 'createdon', 'status')

class EmployeeResource(resources.ModelResource):
    branch = fields.Field(
        column_name='Branch',
        attribute='branch',
        widget=ForeignKeyWidget(Branch, 'name'))
    department = fields.Field(
        column_name='Department',
        attribute='department',
        widget=ForeignKeyWidget(Department, 'name'))
    designation = fields.Field(
        column_name='Designation',
        attribute='designation',
        widget=ForeignKeyWidget(Designation, 'name'))
    '''biometric = fields.Field(
        column_name='biometric_id',
        attribute='biometric_id',
        widget=ForeignKeyWidget(Device, 'name'))
    country = fields.Field(
        column_name='Country',
        attribute='country',
        widget=ForeignKeyWidget(Country, 'name'))
    state = fields.Field(
        column_name='State',
        attribute='state',
        widget=ForeignKeyWidget(State, 'name'))
    city = fields.Field(
        column_name='City',
        attribute='city',
        widget=ForeignKeyWidget(City, 'name'))
    category = fields.Field(
        column_name='Category',
        attribute='caste',
        widget=ForeignKeyWidget(Category, 'name'))
    religion = fields.Field(
        column_name='Religion',
        attribute='religion',
        widget=ForeignKeyWidget(Religion, 'name'))
    bank = fields.Field(
        column_name='Bank',
        attribute='bank',
        widget=ForeignKeyWidget(Bank, 'name'))'''
    class Meta:
        model = Employee
        import_id_fields = ('biometric_id', 'branch')
        exclude = ('id',)
        fields = ('branch','first_name', 'last_name', 'biometric_id', 'doj', 'email','mobile', 'gender','status')



class MyHolidayResource(resources.ModelResource):
    branch = fields.Field(
        column_name='Branch',
        attribute='branch',
        widget=ForeignKeyWidget(Branch, 'name'))
    class Meta:
        model = Holiday
        fields = (
        'id','hdate', 'htitle', 'description','branch')

