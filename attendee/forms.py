from django import forms
from django.forms import TextInput, Select, FileInput
from .models import Employee, Student, Branch, Shifttime


class UserCacheMixin:
    user_cache = None


class EmployeeForm(UserCacheMixin, forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['branch', 'shifttime','reporting_to','probation_period','first_name', 'last_name', 'biometric_id', 'dob', 'doj', 'phone', 'mobile', 'email',
                  'address1', 'address2', 'address3', 'district', 'pincode', 'pan_no', 'aadhar_no', 'bank_account_no',
                  'ifsc_code', 'bank_accountholder_name', 'bank_branch', 'pics', 'city', 'state', 'country',
                  'caste', 'gender', 'marital_status', 'department', 'designation', 'religion', 'bank', 'admin_for',
                  'status']
        widgets = {
            'branch': Select(attrs={'class': 'form-control selectbox'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': u'Please complete your  First Name'}),
            'last_name': TextInput(attrs={'class': 'form-control','required': False}),
            'biometric_id': TextInput(attrs={'class': 'form-control', 'required': False }),
            'dob': TextInput(attrs={'class': 'form-control datepicker','required': False}),
            'doj': TextInput(attrs={'class': 'form-control datepicker'}),
            'phone': TextInput(attrs={'class': 'form-control', 'required': False}),
            'mobile': TextInput(attrs={'class': 'form-control', 'placeholder': u'Please Provide your valid mobile number'}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': u'Provide valid Email Address '}),
            'address1': TextInput(attrs={'class': 'form-control', 'required': False}),
            'address2': TextInput(attrs={'class': 'form-control', 'required': False}),
            'address3': TextInput(attrs={'class': 'form-control ', 'required': False}),
            'district': TextInput(attrs={'class': 'form-control ', 'required': False}),
            'pincode': TextInput(attrs={'class': 'form-control ', 'required': False}),
            'pan_no': TextInput(attrs={'class': 'form-control ', 'required': False}),
            'aadhar_no': TextInput(attrs={'class': 'form-control ', 'required': False}),
            'bank_account_no': TextInput(attrs={'class': 'form-control ', 'required': False}),
            'ifsc_code': TextInput(attrs={'class': 'form-control ', 'required': False}),
            'bank_accountholder_name': TextInput(attrs={'class': 'form-control ', 'required': False}),
            'bank_branch': TextInput(attrs={'class': 'form-control ', 'required': False}),
            'pics': FileInput(attrs={'class': 'form-control ', 'required': False}),
            'city': Select(attrs={'class': 'form-control selectbox', 'required': False}),
            'state': Select(attrs={'class': 'form-control selectbox', 'required': False}),
            'country': Select(attrs={'class': 'form-control selectbox', 'required': False}),
            'caste': Select(attrs={'class': 'form-control selectbox', 'required': False}),
            'gender': Select(attrs={'class': 'form-control selectbox', 'placeholder': u'Select your Gender'}),
            'marital_status': Select(attrs={'class': 'form-control selectbox', 'required': False}),
            'department': Select(attrs={'class': 'form-control selectbox', 'placeholder': u'Select any of given department name'}),
            'designation': Select(attrs={'class': 'form-control selectbox', 'placeholder': u'Select given designation'}),
            'religion': Select(attrs={'class': 'form-control selectbox', 'required': False}),
            'bank': Select(attrs={'class': 'form-control selectbox', 'required': False}),
            'admin_for': Select(attrs={'class': 'form-control selectbox', 'required': False }),
            'shifttime': Select(attrs={'class': 'form-control selectbox', 'required': False}),
            'reporting_to': Select(attrs={'class': 'form-control selectbox','required': False}),
            'probation_period': TextInput(attrs={'class': 'form-control ', 'required': False}),

            'status': Select(attrs={'class': 'form-control selectbox', 'placeholder': u'Select Status '}),

        }

        def __init__(self, *args, **kwargs):
            super(EmployeeForm, self).__init__(*args, **kwargs)
            self.fields['branch'].empty_label = None

        def __init__(self, *args, **kwargs):
            super(EmployeeForm, self).__init__(*args, **kwargs)
            self.fields['shifttime'].empty_label = None

        def __init__(self, *args, **kwargs):
            super(EmployeeForm, self).__init__(*args, **kwargs)
            self.fields['admin_for'].empty_label = None

        def __init__(self, *args, **kwargs):
            super(EmployeeForm, self).__init__(*args, **kwargs)
            self.fields['admin_for'==2].widget.attrs['readonly'] = True




class StudentForm(UserCacheMixin, forms.ModelForm):
    class Meta:
        model = Student
        fields = ['branch', 'batch', 'first_name', 'last_name', 'biometric_id', 'gender', 'dob', 'email', 'mobile',
                  'qualification', 'address1', 'address2', 'pincode', 'aadhar_no', 'profilepic', 'city', 'state',
                  'country', 'status']
        widgets = {
            'branch': Select(attrs={'class': 'form-control selectbox'}),
            'batch': Select(attrs={'class': 'form-control selectbox'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'biometric_id': TextInput(attrs={'class': 'form-control'}),
            'gender': Select(attrs={'class': 'form-control selectbox'}),
            'dob': TextInput(attrs={'class': 'form-control datepicker'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'mobile': TextInput(attrs={'class': 'form-control'}),
            'qualification': TextInput(attrs={'class': 'form-control'}),
            'address1': TextInput(attrs={'class': 'form-control'}),
            'address2': TextInput(attrs={'class': 'form-control'}),
            'pincode': TextInput(attrs={'class': 'form-control'}),
            'aadhar_no': TextInput(attrs={'class': 'form-control'}),
            'profilepic': FileInput(attrs={'class': 'form-control'}),
            'city': Select(attrs={'class': 'form-control selectbox'}),
            'state': Select(attrs={'class': 'form-control selectbox'}),
            'country': Select(attrs={'class': 'form-control selectbox'}),
            'status': Select(attrs={'class': 'form-control selectbox'}),
        }
