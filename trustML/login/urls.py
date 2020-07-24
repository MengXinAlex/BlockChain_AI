from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


from . import views
app_name = 'login'

urlpatterns = [
    path('',  views.index, name='index'),
    # path('', auth_views.LoginView.as_view(), name='login'),
    path('user_profile/', views.editprofile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.editprofile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
