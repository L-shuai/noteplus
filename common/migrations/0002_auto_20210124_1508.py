# Generated by Django 3.1.3 on 2021-01-24 15:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='keyword',
            field=models.CharField(default='关键词', max_length=200),
        ),
        migrations.AlterField(
            model_name='note',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 24, 15, 8, 56, 525796)),
        ),
    ]
