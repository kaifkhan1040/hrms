# Generated by Django 3.0.6 on 2020-07-02 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0019_auto_20200702_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='profilepic',
            field=models.FileField(blank=True, upload_to='documents/'),
        ),
    ]
