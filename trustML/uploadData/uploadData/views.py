from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from .forms import FileFieldForm
from .models import Data,File
from django.conf import settings
import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required(login_url='/')
def index(request):
    path=settings.BASE_DIR+'/media/data/'  # insert the path to your directory
    img_list = [f for f in os.listdir(path)  if f.endswith('.jpeg') or f.endswith('.jpg') or f.endswith('.png')]
    if request.method == 'POST':
        form = FileFieldForm(request.POST, request.FILES)
        files = request.FILES.getlist('file_field')
        for f in files:
            if form.is_valid():
                print('saving',f)
                File(file=f).save()
        # return render(request, 'model.html',{'images': img_list})
        return redirect('/model')
    else:
        form = FileFieldForm()
    return render(request, 'model.html', {'form': form,'images': img_list})


# return render(request,'data.html', {'images': img_list})

# class FileFieldView(FormView):
#     form_class = FileFieldForm
#     template_name = 'upload.html'  # Replace with your template.
#     success_url = '/'  # Replace with your URL or reverse().
#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         files = request.FILES.getlist('file_field')
#         if form.is_valid():
#             for f in files:
#                 File(file=f)
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
