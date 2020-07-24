""" This python file handles all the request relative to data upload

"""
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from .forms import FileFieldForm
from .models import Data, File
from django.conf import settings
import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required(login_url='/')
def index(request):
    """
    :param request:
    :return:
    """
    path = settings.BASE_DIR + '/media/data/'  # insert the path to your directory
    img_list = [f for f in os.listdir(path) if f.endswith('.jpeg') or f.endswith('.jpg') or f.endswith('.png')]
    if request.method == 'POST':
        form = FileFieldForm(request.POST, request.FILES)
        files = request.FILES.getlist('file_field')
        for f in files:
            if form.is_valid():
                print('saving', f)
                File(file=f).save()
        # return render(request, 'model.html',{'images': img_list})
        return redirect('/model')
    else:
        form = FileFieldForm()
    return render(request, 'model.html', {'form': form, 'images': img_list})
