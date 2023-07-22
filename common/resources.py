from import_export import  fields,resources
from import_export.widgets import ForeignKeyWidget
from .models import Country,State,City,Religion,Category,Bank,Department,Designation,Course

class CountryResource(resources.ModelResource):
    class Meta:
        model = Country

class StateResource(resources.ModelResource):
        country = fields.Field(
            column_name='Country',
            attribute='country',
            widget=ForeignKeyWidget(Country, 'name'))
        class Meta:
            model = State
            fields = ('id','country','name','status')


class CityResource(resources.ModelResource):
    state = fields.Field(
        column_name='State',
        attribute='state',
        widget=ForeignKeyWidget(State, 'name'))

    class Meta:
        model = City
        fields = ('state', 'name')

class ReligionResource(resources.ModelResource):
    class Meta:
        model = Religion

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category

class BankResource(resources.ModelResource):
    class Meta:
        model = Bank

class DepartmentResource(resources.ModelResource):
    class Meta:
        model = Department

class DesignationResource(resources.ModelResource):
    class Meta:
        model = Designation

class CourseResource(resources.ModelResource):
    class Meta:
        model = Course
