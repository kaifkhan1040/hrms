# Generated by Django 3.0.6 on 2020-07-03 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0024_auto_20200703_0623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qualification',
            name='document',
            field=models.FileField(blank=True, upload_to='content/media/documents/'),
        ),
    ]
