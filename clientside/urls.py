"""clientside URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from client import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.userregister,name='register'),
    path('login/',views.userlogin,name='login'),
    path('logout/',views.userlogout,name='logout'),
    path('profile/',views.userprofile,name='profile'),
    path('plans/',views.plans,name='plans'),
    path('plans/<int:days>',views.plans,name='plans'),
    path('getdata/<str:day>',views.getdata,name='plans'),
]
