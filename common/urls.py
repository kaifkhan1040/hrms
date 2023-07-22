from django.urls import path
from common import views
from .views import (
    CountryListView,CountryCreate,CountryUpdate,CountryDelete,
StateListView,StateCreate,StateUpdate,StateDelete,
CityListView,CityCreate,CityUpdate,CityDelete,
ReligionListView,ReligionCreate,ReligionUpdate,ReligionDelete,
CategoryListView,CategoryCreate,CategoryUpdate,CategoryDelete,
BankListView,BankCreate,BankUpdate,BankDelete,
DepartmentListView,DepartmentCreate,DepartmentUpdate,DepartmentDelete,
DesignationListView,DesignationCreate,DesignationUpdate,DesignationDelete,
CourseListView,CourseCreate,CourseUpdate,CourseDelete
)

app_name = 'common'
urlpatterns = [
    path('country/', CountryListView.as_view(), name='country'),
    path('country/add', CountryCreate.as_view(), name='country_create'),
    path('country/edit/<int:pk>', CountryUpdate.as_view(), name='country_edit'),
    path('country/delete/<int:pk>', CountryDelete.as_view(), name='country_delete'),

    path('state/', StateListView.as_view(), name='state'),
    path('state/add', StateCreate.as_view(), name='state_create'),
    path('state/edit/<int:pk>', StateUpdate.as_view(), name='state_edit'),
    path('state/delete/<int:pk>', StateDelete.as_view(), name='state_delete'),

    path('city/', CityListView.as_view(), name='city'),
    path('city/add', CityCreate.as_view(), name='city_create'),
    path('city/edit/<int:pk>', CityUpdate.as_view(), name='city_edit'),
    path('city/delete/<int:pk>', CityDelete.as_view(), name='city_delete'),

    path('religion/', ReligionListView.as_view(), name='religion'),
    path('religion/add', ReligionCreate.as_view(), name='religion_create'),
    path('religion/edit/<int:pk>', ReligionUpdate.as_view(), name='religion_edit'),
    path('religion/delete/<int:pk>', ReligionDelete.as_view(), name='religion_delete'),

    path('category/', CategoryListView.as_view(), name='category'),
    path('category/add', CategoryCreate.as_view(), name='category_create'),
    path('category/edit/<int:pk>', CategoryUpdate.as_view(), name='category_edit'),
    path('category/delete/<int:pk>', CategoryDelete.as_view(), name='category_delete'),

    path('bank/', BankListView.as_view(), name='bank'),
    path('bank/add', BankCreate.as_view(), name='bank_create'),
    path('bank/edit/<int:pk>', BankUpdate.as_view(), name='bank_edit'),
    path('bank/delete/<int:pk>', BankDelete.as_view(), name='bank_delete'),

    path('department/', DepartmentListView.as_view(), name='department'),
    path('department/add', DepartmentCreate.as_view(), name='department_create'),
    path('department/edit/<int:pk>', DepartmentUpdate.as_view(), name='department_edit'),
    path('department/delete/<int:pk>', DepartmentDelete.as_view(), name='department_delete'),

    path('designation/', DesignationListView.as_view(), name='designation'),
    path('designation/add', DesignationCreate.as_view(), name='designation_create'),
    path('designation/edit/<int:pk>', DesignationUpdate.as_view(), name='designation_edit'),
    path('designation/delete/<int:pk>', DesignationDelete.as_view(), name='designation_delete'),

    path('course/', CourseListView.as_view(), name='course'),
    path('course/add', CourseCreate.as_view(), name='course_create'),
    path('course/edit/<int:pk>', CourseUpdate.as_view(), name='course_edit'),
    path('course/delete/<int:pk>', CourseDelete.as_view(), name='course_delete'),


    path('export_country/',views.export_country, name='export_country'),
    path('export_state/', views.export_state, name='export_state'),
    path('export_city/', views.export_city, name='export_city'),
    path('export_religion/', views.export_religion, name='export_religion'),
    path('export_bank/', views.export_bank, name='export_bank'),
    path('export_category/', views.export_category, name='export_category'),
    path('export_department/', views.export_department, name='export_department'),
    path('export_designation/', views.export_designation, name='export_designation'),
    path('export_course/', views.export_course, name='export_course'),

    path('import-country/',views.import_country, name='import_country'),
    path('import-state/', views.import_state, name='import_state'),
    path('import-city/', views.import_city, name='import_city'),
    path('import-religion/', views.import_religion, name='import_religion'),
    path('import-bank/', views.import_bank, name='import_bank'),
    path('import-category/', views.import_category, name='import_category'),
    path('import-department/', views.import_department, name='import_department'),
    path('import-designation/', views.import_designation, name='import_designation'),
    path('import-course/', views.import_course, name='import_course'),
]