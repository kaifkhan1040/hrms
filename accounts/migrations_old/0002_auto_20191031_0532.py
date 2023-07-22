# Generated by Django 2.1.9 on 2019-10-31 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='personal_email',
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]