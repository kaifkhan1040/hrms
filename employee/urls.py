from django.urls import path
from common import views
from .views import (
BankListView,BankCreate,BankUpdate,BankDelete,
)

app_name = 'employee'
urlpatterns = [
    path('bank/', BankListView.as_view(), name='bank'),
    path('bank/add', BankCreate.as_view(), name='bank_create'),
    path('bank/edit/<int:pk>', BankUpdate.as_view(), name='bank_edit'),
    path('bank/delete/<int:pk>', BankDelete.as_view(), name='bank_delete'),
]