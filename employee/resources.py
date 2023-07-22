from import_export import  fields,resources
from import_export.widgets import ForeignKeyWidget
from .models import Bank

class BankResource(resources.ModelResource):
    class Meta:
        model = Bank