# Generated by Django 2.1.9 on 2020-02-26 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_applicant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='applicant',
        ),
    ]
