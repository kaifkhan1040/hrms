# Generated by Django 2.1.9 on 2020-02-07 10:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_auto_20200207_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='fordate',
            field=models.DateField(default=datetime.date.today, verbose_name='Date'),
        ),
    ]