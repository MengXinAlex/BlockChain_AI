from django import forms
from .models import  Data
class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ['description','data_file','data_type','uploader','relative_model']

class editDataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ['model_score', 'data_score']