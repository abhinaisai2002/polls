# Generated by Django 3.0.7 on 2021-06-13 17:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20210613_2259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentby',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
