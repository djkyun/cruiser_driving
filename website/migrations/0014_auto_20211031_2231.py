# Generated by Django 3.1.1 on 2021-10-31 14:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_auto_20211031_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrecords',
            name='datetime_registered',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 31, 37, 23830)),
        ),
    ]
