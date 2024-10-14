from django.contrib import admin
from django.urls import path
from .views.auth_views import login,logout
from .views.user_views import dashboard


urlpatterns = [
    path('app2',login,name="login"),
    path('app2/login',login,name="login"),
    path('logout',logout,name="logout"),
    path('dashboard',dashboard,name="dashboard"),


   

]