# Generated by Django 3.0.4 on 2020-03-26 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0006_employee_shifttime'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='reporting_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='attendee.Employee'),
        ),
    ]
