from django.test import TestCase
from uploadData.models import Data
from login.models import User
from .models import ML_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File


def create_user(t_email, t_password):
    return User.objects.create(email=t_email, password=t_password)

def upload_data(user, description, data, model):
    return Data.objects.create(uploader=user, relative_model=model, data_file=data, description=description)

def upload_model(user, name, model, specification):
    return ML_model.objects.create(creator=user, model_name=name, model_file=model, specification=specification)

class test_data_and_model(TestCase):
    def test_model_upload(self):
        model = File(open('/Users/eamonhugh/Desktop/UNITWERK/y3/s2/soft3413/p03/trustML/media/testData/model_1', 'rb'))
        specification = File(open('/Users/eamonhugh/Desktop/UNITWERK/y3/s2/soft3413/p03/trustML/media/testData/specification.json', 'rb'))
        user = create_user('eamon@test.com','11aaBB!!')
        uploaded_model = upload_model(user, 'test model', model, specification)
        self.assertIs(uploaded_model.model_name, 'test model')

    def test_data_upload(self):
        data = File(open('/Users/eamonhugh/Desktop/UNITWERK/y3/s2/soft3413/p03/trustML/media/testData/data_training_average.csv', 'rb'))
        model = File(open('/Users/eamonhugh/Desktop/UNITWERK/y3/s2/soft3413/p03/trustML/media/testData/model_1', 'rb'))
        specification = File(open('/Users/eamonhugh/Desktop/UNITWERK/y3/s2/soft3413/p03/trustML/media/testData/specification.json', 'rb'))
        user = create_user('eamon@test.com','11aaBB!!')
        uploaded_model = upload_model(user, 'test model', model, specification)
        uploaded_data = upload_data(user, 'test description', data, uploaded_model)
        self.assertIs(uploaded_data.description, 'test description')
