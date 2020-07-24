# Generated by Django 2.2.1 on 2019-05-27 01:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadData', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation_result',
            name='accset',
            field=models.CharField(default=[0, 0, 0, 0, 0], max_length=10000, validators=[django.core.validators.int_list_validator]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evaluation_result',
            name='uncset',
            field=models.CharField(default=[0, 0, 0, 0, 0], max_length=10000, validators=[django.core.validators.int_list_validator]),
            preserve_default=False,
        ),
    ]