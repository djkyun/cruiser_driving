# Generated by Django 3.1.1 on 2021-10-20 19:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20211021_0308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrecords',
            name='datetime_registered',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 21, 3, 43, 30, 534547)),
        ),
    ]
