# Generated by Django 2.2.1 on 2019-06-05 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadData', '0003_auto_20190605_0711'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation_result',
            name='data_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='evaluation_result',
            name='model_score',
            field=models.IntegerField(default=0),
        ),
    ]
