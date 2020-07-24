from django.urls import path

from . import views

app_name = 'upload_model'
urlpatterns = [
    path('delete_model/<int:model_id>', views.delete_model, name = 'delete_model'),
    path('home/', views.home, name='home'),
    path('model_detail/<int:model_id>/',views.model_detail, name='model_detail'),
    path('buy_model_detail/<int:model_id>/',views.buy_model_detail, name='buy_model_detail'),
    path('download_model/<int:model_id>/',views.download_model, name='download_model'),
    path('uploading/',views.uploading,name='uploading'),
    path('upload_data_evaluate/<int:data_pk>/',views.upload_data_evaluate,name='upload_data_evaluate'),
    path('upload_data/',views.upload_data,name="upload_data"),
    path('test/', views.test, name='test'),
    path('error/', views.error, name='error'),
    path('error_data/', views.error_data, name='error_data'),
    path('reward//<str:receiver>/<int:id>/<int:value>', views.reward, name='reward'),
]
