from django import forms
import numpy as np
from .models import ML_model
class ModelForm(forms.ModelForm):
    class Meta:
        model = ML_model
        #fields = ['model_name','model_file','specification','trainingData','label','creator']
        fields = ['model_name','model_file','specification','trainingData','label','creator',"split_data","split_model"]
    # def clean(self):
    #     clean_data = super(ModelForm,self).clean()
    #     weights = np.genfromtxt(clean_data.get('weight'),delimiter=',',dtype=float)
    #     for weight in weights[1]:
    #         # the weight cannot be negative
    #         if weight < 0:
    #             raise ValueError("Negative weights")
    #     return clean_data
