# Generated by Django 3.0.6 on 2020-06-29 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0012_auto_20200406_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='address',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
