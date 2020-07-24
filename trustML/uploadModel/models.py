from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.utils import timezone
import os

class ML_model(models.Model):
    creation_time = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    model_name = models.CharField(max_length=100,null = False)
    model_file = models.FileField(upload_to='ML_models/')
    specification = models.FileField(upload_to = 'ML_specifications/')
    trainingData = models.FileField(upload_to = 'ML_trainingData/')
    label = models.FileField(upload_to = 'ML_label/')
    split_data = models.FloatField(default = 0.2)
    split_model = models.FloatField(default  = 0.8)
    # weight = models.FileField(upload_to='ML_weights/')

@receiver(models.signals.post_delete, sender=ML_model)
def auto_delete_file_on_delete_ML_model(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.model_file:
        if os.path.isfile(instance.model_file.path):
            os.remove(instance.model_file.path)
    if instance.specification:
        if os.path.isfile(instance.specification.path):
            os.remove(instance.specification.path)
    if instance.trainingData:
        if os.path.isfile(instance.trainingData.path):
            os.remove(instance.trainingData.path)
    if instance.label:
        if os.path.isfile(instance.label.path):
            os.remove(instance.label.path)
