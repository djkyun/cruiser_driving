# Generated by Django 3.1.1 on 2021-10-29 19:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_auto_20211030_0342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrecords',
            name='datetime_registered',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 30, 3, 43, 36, 3397)),
        ),
    ]
