# Generated by Django 3.1.3 on 2021-01-27 11:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20210124_1703'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='author',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='note',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 27, 11, 15, 0, 432808)),
        ),
    ]