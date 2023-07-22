from datetime import timedelta

from django import forms
from django.forms import ValidationError,TextInput,Select
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .models  import Bank
class UserCacheMixin:
    user_cache = None


class BankForm(UserCacheMixin, forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['name','status']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control selectbox'}),
        }