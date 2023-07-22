# Generated by Django 3.0.6 on 2020-11-25 06:47

import attendee.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        ('hierarchy', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biometric_id', models.CharField(max_length=50, null=True, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('studentslug', models.CharField(blank=True, max_length=50, null=True)),
                ('gender', models.IntegerField(blank=True, choices=[(1, 'Male'), (0, 'Female')])),
                ('dob', models.CharField(blank=True, max_length=50, null=True)),
                ('doj', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('mobile', models.CharField(blank=True, max_length=50, null=True)),
                ('qualification', models.CharField(blank=True, max_length=50, null=True)),
                ('address1', models.CharField(blank=True, max_length=50, null=True)),
                ('address2', models.CharField(blank=True, max_length=50, null=True)),
                ('pincode', models.CharField(blank=True, max_length=50, null=True)),
                ('aadhar_no', models.CharField(blank=True, max_length=50, null=True)),
                ('profilepic', models.FileField(blank=True, upload_to='documents/')),
                ('createdon', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(blank=True, choices=[(1, 'Active'), (0, 'In-Active')])),
                ('batch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hierarchy.Batch')),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hierarchy.Branch')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.City')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.Country')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.State')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_of', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(blank=True, upload_to='documents/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('employeeslug', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('biometric_id', models.CharField(blank=True, max_length=50, null=True)),
                ('dob', models.CharField(blank=True, max_length=50, null=True)),
                ('doj', models.CharField(blank=True, help_text='Select joining date of employee', max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('mobile', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('address1', models.CharField(blank=True, max_length=50, null=True)),
                ('address2', models.CharField(blank=True, max_length=50, null=True)),
                ('address3', models.CharField(blank=True, max_length=50, null=True)),
                ('district', models.CharField(blank=True, max_length=50, null=True)),
                ('pincode', models.CharField(blank=True, max_length=50, null=True)),
                ('pan_no', models.CharField(blank=True, max_length=50, null=True)),
                ('aadhar_no', models.CharField(blank=True, max_length=50, null=True)),
                ('bank_account_no', models.CharField(blank=True, max_length=50, null=True)),
                ('ifsc_code', models.CharField(blank=True, max_length=50, null=True)),
                ('bank_accountholder_name', models.CharField(blank=True, max_length=50, null=True)),
                ('bank_branch', models.CharField(blank=True, max_length=50, null=True)),
                ('pics', models.FileField(blank=True, upload_to=attendee.models.get_file_path)),
                ('gender', models.IntegerField(blank=True, choices=[(1, 'Male'), (0, 'Female')], help_text='Select gender of employee', null=True)),
                ('marital_status', models.IntegerField(blank=True, choices=[(1, 'Married'), (0, 'Un-Married')], null=True)),
                ('createdon', models.DateTimeField(auto_now_add=True)),
                ('admin_for', models.IntegerField(blank=True, choices=[(1, 'Organisation'), (2, 'Branch'), (0, 'None')], help_text='Select and authorize an Employee ', null=True)),
                ('status', models.IntegerField(blank=True, choices=[(1, 'Active'), (0, 'In-Active')], help_text='Select status of employee', null=True)),
                ('experience', models.CharField(blank=True, max_length=50, null=True)),
                ('profile', models.ImageField(blank=True, null=True, upload_to='')),
                ('probation_period', models.IntegerField(blank=True, default=0, help_text='allocate no. of day for probation period', null=True)),
                ('bank', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.Bank')),
                ('branch', models.ForeignKey(blank=True, help_text='Select branch', null=True, on_delete=django.db.models.deletion.SET_NULL, to='hierarchy.Branch')),
                ('caste', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.Category')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.City')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.Country')),
                ('department', models.ForeignKey(blank=True, help_text='Select Department for employee', null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.Department')),
                ('designation', models.ForeignKey(blank=True, help_text='Select designation for employee', null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.Designation')),
                ('religion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.Religion')),
                ('reporting_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='attendee.Employee')),
                ('shifttime', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hierarchy.Shifttime')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.State')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]