# Generated by Django 3.0.4 on 2020-03-30 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0007_regularisation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='regularisation',
            old_name='description',
            new_name='reason',
        ),
    ]