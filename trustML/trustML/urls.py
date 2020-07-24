"""trustML URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', include('login.urls')),
    # path('',  views.index, name='index'),
    # needed for login page
    path('', include('django.contrib.auth.urls')),
    path('user_home/', views.user_home, name='user_home'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('help/', views.help, name='help'),
    path('wallet/', views.wallet, name='wallet'),
    path('buy_model/', views.buy_model, name='buy_model'),
    path('admin/', admin.site.urls),
    path('models/',include('uploadModel.urls')),
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login')
]
