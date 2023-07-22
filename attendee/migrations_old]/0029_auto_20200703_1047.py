# Generated by Django 3.0.6 on 2020-07-03 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0028_auto_20200703_0652'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='profilepic',
        ),
        migrations.AddField(
            model_name='employee',
            name='pics',
            field=models.FileField(blank=True, upload_to='get_file_path'),
        ),
        migrations.AlterField(
            model_name='student',
            name='profilepic',
            field=models.FileField(blank=True, upload_to='documents/'),
        ),
    ]