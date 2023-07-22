from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
GN = (
    (1, 'Organisation'),
    (2, 'Branch'),
)

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    editor_type = models.IntegerField(default=False) #1.Organisation Admin 2. Branch Admin
    editor_typeid = models.IntegerField(choices=GN,default=False) #Organisation ID / Branch ID
    personal_email = models.CharField(max_length=75,blank=True,null=True)
    profile_pic = models.CharField(max_length=200,blank=True,null=True)

class Activation(models.Model):
    user =models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)


