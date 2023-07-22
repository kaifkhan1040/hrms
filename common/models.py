from django.db import models

ST = (
    (1, 'Active'),
    (0, 'In-Active'),
)
class Country(models.Model):

    name = models.CharField(max_length=200,unique=True)
    status = models.IntegerField(choices=ST,blank=True)

    def __str__(self):
        return self.name

class State(models.Model):
    country = models.ForeignKey(Country,models.SET_NULL,blank=True,null=True)
    name = models.CharField(max_length=200, unique=True)
    status = models.IntegerField(choices=ST,blank=True)

    def __str__(self):
        return self.name

class City(models.Model):
    state = models.ForeignKey(State,models.SET_NULL,blank=True,null=True)
    name = models.CharField(max_length=200, unique=True)
    status = models.IntegerField(choices=ST,blank=True)

    def __str__(self):
        return self.name

class Religion(models.Model):
    name = models.CharField(max_length=200, unique=True)
    status = models.IntegerField(choices=ST,blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    status = models.IntegerField(choices=ST,blank=True)

    def __str__(self):
        return self.name

class Bank(models.Model):
    name = models.CharField(max_length=200, unique=True)
    status = models.IntegerField(choices=ST,blank=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=200, unique=True)
    status = models.IntegerField(choices=ST,blank=True)

    def __str__(self):
        return self.name

class Designation(models.Model):
    department = models.ForeignKey(Department, models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=200, unique=True)
    status = models.IntegerField(choices=ST,blank=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=200, unique=True)
    status = models.IntegerField(choices=ST,blank=True)

    def __str__(self):
        return self.name