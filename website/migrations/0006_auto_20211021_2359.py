# Generated by Django 3.1.1 on 2021-10-21 15:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_auto_20211021_0347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrecords',
            name='datetime_registered',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 21, 23, 59, 22, 75448)),
        ),
    ]
