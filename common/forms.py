from datetime import timedelta

from django import forms
from django.forms import ValidationError, TextInput, Select
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .models import Country, State, City, Religion, Bank, Category, Department, Designation, Course


class UserCacheMixin:
    user_cache = None


class CountryForm(UserCacheMixin, forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name', 'status']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control selectbox'}),
        }


class StateForm(UserCacheMixin, forms.ModelForm):
    class Meta:
        model = State
        fields = ['name', 'country', 'status']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'country': Select(attrs={'class': 'form-control selectbox selectbox'}),
            'status': Select(attrs={'class': 'form-control selectbox selectbox'}),
        }


class CityForm(UserCacheMixin, forms.ModelForm):
    class Meta:
        model = City
        fields = ['name', 'state', 'status']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'state': Select(attrs={'class': 'form-control selectbox'}),
            'status': Select(attrs={'class': 'form-control selectbox'}),
        }


class ReligionForm(UserCacheMixin, forms.ModelForm):
    class Meta:
        model = Religion
        fields = ['name', 'status']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control selectbox'}),
        }


class BankForm(UserCacheMixin, forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['name', 'status']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control selectbox'}),
        }


class CategoryForm(UserCacheMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'status']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control selectbox'}),
        }


class DepartmentForm(UserCacheMixin, forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'status']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control selectbox'}),
        }


class DesignationForm(UserCacheMixin, forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['name', 'department', 'status']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'department': Select(attrs={'class': 'form-control selectbox selectbox'}),
            'status': Select(attrs={'class': 'form-control selectbox selectbox'}),

        }


class CourseForm(UserCacheMixin, forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'status']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control selectbox'}),
        }
