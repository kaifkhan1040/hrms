from django import forms
from django.forms import TextInput, Select, FileInput, RadioSelect
from .models import Attendance, Regularisation

class UserCacheMixin:
    user_cache = None


class EmployeeattendanceForm(UserCacheMixin, forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['user','event_hh','event_mm','event_ss','event_type','lattitude','longitude','fordate']
        widgets = {
            'user': Select(attrs={'class':'form-control ','readonly':'readonly'}),
            'event_hh': Select(attrs={'class':'form-control'}),
            'event_mm': Select(attrs={'class': 'form-control'}),
            'event_ss': Select(attrs={'class': 'form-control'}),
            'event_type': Select(attrs={'class': 'form-control'}),
            'lattitude': TextInput(attrs={'class': 'form-control'}),
            'longitude': TextInput(attrs={'class': 'form-control'}),
            'fordate': TextInput(attrs={'class': 'form-control datepicker'}),
        }

class StudentattendanceForm(UserCacheMixin, forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['user','event_hh','event_mm','event_ss','event_type','lattitude','longitude','fordate']
        widgets = {
            'user': Select(attrs={'class':'form-control ','readonly':'readonly'}),
            'event_hh': Select(attrs={'class': 'form-control'}),
            'event_mm': Select(attrs={'class': 'form-control'}),
            'event_ss': Select(attrs={'class': 'form-control'}),
            'event_type': Select(attrs={'class': 'form-control'}),
            'lattitude': TextInput(attrs={'class': 'form-control'}),
            'longitude': TextInput(attrs={'class': 'form-control'}),
            'fordate': TextInput(attrs={'class': 'form-control datepicker'}),
        }

class RegularisationForm(UserCacheMixin, forms.ModelForm):
    class Meta:
        model = Regularisation
        fields = ['date','starttime_hh','starttime_mm','endtime_hh','endtime_mm','applying_for', 'reason']
        widgets = {
            'date': TextInput(attrs={'class': 'form-control datepicker'}),
            'starttime_hh': Select(attrs={'class': 'form-control'}),
            'starttime_mm': Select(attrs={'class': 'form-control'}),
            'endtime_hh': Select(attrs={'class': 'form-control'}),
            'endtime_mm': Select(attrs={'class': 'form-control'}),
            'applying_for': Select(attrs={'class': 'form-control'}),
            'reason': TextInput(attrs={'class': 'form-control'}),
        }









