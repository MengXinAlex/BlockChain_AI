# Generated by Django 2.1.2 on 2018-10-30 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('uploadModel', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('data_file', models.FileField(upload_to='data/')),
                ('data_type', models.CharField(choices=[('OR', 'Original'), ('TE', 'Test')], default='TE', max_length=2)),
                ('relative_model', models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='uploadModel.ML_model')),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='evaluation_result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result_type', models.CharField(choices=[('MD', 'Model_result'), ('DT', 'data_result')], default='DT', max_length=2)),
                ('similarity', models.FloatField(null=True)),
                ('score', models.FloatField(null=True)),
                ('result', models.FileField(upload_to='evaluation_result/')),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('document_count', models.IntegerField(default=0)),
                ('data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uploadData.Data')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uploadModel.ML_model')),
            ],
            options={
                'ordering': ['creation_time'],
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('file', models.FileField(upload_to='data/')),
            ],
        ),
    ]
