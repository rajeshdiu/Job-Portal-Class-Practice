# Generated by Django 5.0 on 2023-12-20 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0005_recruiterprofile_user_jobseekerprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobseekerprofile',
            name='skills',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
