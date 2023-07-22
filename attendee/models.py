import os

import boto3
from botocore.exceptions import NoCredentialsError
from django.core.files.storage import FileSystemStorage
from django.db import models
from common.models import Country,State,City,Department,Designation,Category,Religion,Bank
from django.contrib.auth.models import User
from hierarchy.models import Organisation,Branch,Batch,Device, Shifttime
from django.conf import settings

from app.conf.development.settings import MEDIA_ROOT

ST = (
    (1, 'Active'),
    (0, 'In-Active'),
)
YN = (
    (1, 'Yes'),
    (0, 'No'),
)
FC = (
    (1, 'Organisation'),
    (2, 'Branch'),
    (0, 'None'),
)
MS = (
    (1, 'Married'),
    (0, 'Un-Married'),
)
GN = (
    (1, 'Male'),
    (0, 'Female'),
)
LR = (
    (1, 'Lok Sabha'),
    (2, 'Rajya Sabha'),
)

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.user.username , ext)
    fs = os.path.join(MEDIA_ROOT + '/employeepics/' + filename )
    return fs


class Employee(models.Model):
    class Meta:
        ordering = ('-id',)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.ForeignKey(Branch, models.SET_NULL, blank=True, null=True, help_text='Select branch')
    shifttime = models.ForeignKey(Shifttime, models.SET_NULL, blank=True, null=True)
    reporting_to = models.ForeignKey("Employee",  on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=50,blank=True,null=True)
    employeeslug = models.CharField(max_length=50,blank=True,null=True)
    last_name = models.CharField(max_length=50,blank=True,null=True)
    biometric_id = models.CharField(max_length=50,blank=True,null=True)
    dob = models.CharField(max_length=50,blank=True,null=True)
    doj = models.CharField(max_length=50,blank=True,null=True, help_text='Select joining date of employee')
    phone = models.CharField(max_length=50,blank=True,null=True)
    mobile = models.CharField(max_length=50,blank=True,null=True)
    email = models.CharField(max_length=50,blank=True,null=True)
    address1 = models.CharField(max_length=50,blank=True,null=True)
    address2 = models.CharField(max_length=50,blank=True,null=True)
    address3 = models.CharField(max_length=50,blank=True,null=True)
    district = models.CharField(max_length=50,blank=True,null=True)
    pincode = models.CharField(max_length=50,blank=True,null=True)
    pan_no = models.CharField(max_length=50,blank=True,null=True)
    aadhar_no = models.CharField(max_length=50,blank=True,null=True)
    bank_account_no = models.CharField(max_length=50,blank=True,null=True)
    ifsc_code = models.CharField(max_length=50,blank=True,null=True)
    bank_accountholder_name = models.CharField(max_length=50,blank=True,null=True)
    bank_branch = models.CharField(max_length=50,blank=True,null=True)
    pics = models.FileField(upload_to=get_file_path, blank=True)
    city = models.ForeignKey(City,models.SET_NULL,blank=True,null=True)
    state = models.ForeignKey(State, models.SET_NULL, blank=True, null=True)
    country = models.ForeignKey(Country, models.SET_NULL, blank=True, null=True)
    caste = models.ForeignKey(Category, models.SET_NULL, blank=True, null=True)
    gender = models.IntegerField(choices=GN, blank=True, null=True, help_text='Select gender of employee')
    marital_status = models.IntegerField(choices=MS, blank=True, null=True)
    department = models.ForeignKey(Department, models.SET_NULL, blank=True, null=True, help_text='Select Department for employee')
    designation = models.ForeignKey(Designation, models.SET_NULL, blank=True, null=True, help_text='Select designation for employee')
    religion = models.ForeignKey(Religion, models.SET_NULL, blank=True, null=True)
    bank = models.ForeignKey(Bank, models.SET_NULL, blank=True, null=True)
    createdon = models.DateTimeField(auto_now_add=True)
    admin_for = models.IntegerField(choices=FC, blank=True, null=True , help_text='Select and authorize an Employee ')
    status = models.IntegerField(choices=ST,blank=True, null=True, help_text='Select status of employee')
    experience = models.CharField(max_length=50,blank=True,null=True)
    profile = models.ImageField(blank=True,null=True)
    probation_period = models.IntegerField(default=0, blank=True,null=True,help_text='allocate no. of day for probation period')
    #probation_period1 = models.IntegerField(default=0, blank=True,null=True,help_text='allocate no. of day for probation period')


    #def __str__(self):
     # return print(f'%s %s',self.first_name,self.last_name)
    def __str__(self):
        return self.first_name



class Student(models.Model):
    class Meta:
        ordering = ('-id',)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    branch =  models.ForeignKey(Branch, models.SET_NULL, blank=True, null=True)
    batch = models.ForeignKey(Batch, models.SET_NULL, blank=True, null=True)
    biometric_id = models.CharField(max_length=50,unique=True, null=True)
    first_name = models.CharField(max_length=50,blank=True,null=True)
    last_name = models.CharField(max_length=50,blank=True,null=True)
    studentslug = models.CharField(max_length=50, blank=True, null=True)
    gender = models.IntegerField(choices=GN, blank=True)
    dob = models.CharField(max_length=50,blank=True,null=True)
    doj = models.CharField(max_length=50,blank=True,null=True)
    email = models.CharField(max_length=50,blank=True,null=True)
    mobile = models.CharField(max_length=50,blank=True,null=True)
    qualification = models.CharField(max_length=50,blank=True,null=True)
    address1 = models.CharField(max_length=50,blank=True,null=True)
    address2 = models.CharField(max_length=50,blank=True,null=True)
    pincode = models.CharField(max_length=50,blank=True,null=True)
    aadhar_no = models.CharField(max_length=50,blank=True,null=True)
    profilepic = models.FileField(upload_to='documents/',blank=True)
    createdon = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ST, blank=True)
    city = models.ForeignKey(City, models.SET_NULL, blank=True, null=True)
    state = models.ForeignKey(State, models.SET_NULL, blank=True, null=True)
    country = models.ForeignKey(Country, models.SET_NULL, blank=True, null=True)

    #def __str__(self):
     #  return print(f'%s %s',self.first_name,self.last_name)



class Qualification(models.Model):

    document_of = models.CharField(max_length=50,blank=True,null=True)
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/',blank=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

