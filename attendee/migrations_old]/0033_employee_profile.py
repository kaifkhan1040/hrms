# Generated by Django 3.0.6 on 2020-07-19 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0032_remove_employee_emppics'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='profile',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]