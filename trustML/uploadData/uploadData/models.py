from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from uploadModel.models import ML_model
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import int_list_validator
import os

# Create your models here.
class Data(models.Model):
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    relative_model = models.ForeignKey(ML_model, on_delete = models.CASCADE,default = 0, null=True)
    description = models.CharField(max_length=255, blank=True)
    data_file = models.FileField(upload_to='data/')
    ORIGINIAL = 'OR'
    TEST = 'TE'
    DATA_TYPE_CHOICE = (
        (ORIGINIAL,'Original'),
        (TEST, 'Test')
    )
    data_type = models.CharField(max_length= 2 , choices= DATA_TYPE_CHOICE, default= TEST)

class File(models.Model):
    description = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='data/')

class evaluation_result(models.Model):
    model = models.ForeignKey(ML_model, on_delete=models.CASCADE)
    data = models.ForeignKey(Data, on_delete = models.CASCADE)
    MODEL = 'MD'
    DATA = 'DT'
    RESULT_TYPE_CHOICE = (
        (MODEL,'Model_result'),
        (DATA,'data_result')
    )
    result_type = models.CharField(max_length=2, choices=RESULT_TYPE_CHOICE,default = DATA)
    # if it's data -> similarity cannot be blank if it's model -> similiarity is blank
    similarity = models.FloatField(null=True)
    # the result is always a confusion matrix file in numpy format
    result = models.FileField(upload_to="evaluation_result/",null=False)
    creation_time = models.DateTimeField(default=timezone.now)
    document_count = models.IntegerField(null=False, default= 0)
    accset = models.CharField(validators=int_list_validator)
    uncset = models.CharField(validators=int_list_validator)
    class Meta:
        ordering = ['creation_time']

@receiver(models.signals.post_delete, sender=evaluation_result)
def auto_delete_file_on_delete_evaluation_result(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.result:
        if os.path.isfile(instance.result.path):
            os.remove(instance.result.path)

@receiver(models.signals.post_delete, sender=Data)
def auto_delete_file_on_delete_Data(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.result:
        if os.path.isfile(instance.data_file.path):
            os.remove(instance.data_file.path)
