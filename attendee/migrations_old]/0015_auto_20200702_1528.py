# Generated by Django 3.0.6 on 2020-07-02 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0014_auto_20200610_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='profilepic',
            field=models.FileField(blank=True, null=True, upload_to='profilepics/'),
        ),
    ]
