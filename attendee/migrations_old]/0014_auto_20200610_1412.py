# Generated by Django 3.0.6 on 2020-06-10 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0013_auto_20200610_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='profilepic',
            field=models.FileField(blank=True, upload_to='documents/'),
        ),
        migrations.AlterField(
            model_name='student',
            name='profilepic',
            field=models.FileField(blank=True, upload_to='documents/'),
        ),
    ]