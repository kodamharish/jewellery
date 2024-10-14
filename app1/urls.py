from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',login,name="login"),
    path('login',login,name="login"),
    path('logout',logout,name="logout"),

    path('dashboard',dashboard,name="dashboard"),

    path('installment_remainder',installment_remainder,name="installment_remainder"),
    path('member_details',member_details,name="member_details"),
    path('recepit/',recepit,name="recepit"),
    path('add_member',add_member,name="add_member"),
    path('add_scheme',add_scheme,name="add_scheme"),
    path('add_group',add_group,name="add_group"),


    path('add_nominee',add_nominee,name="add_nominee"),
    path('tag',tag,name="tag"),
    path('barcode/<str:member_id>/', generate_member_barcode, name='generate_member_barcode'),
    path('member/<str:member_id>/', member_detail_with_barcode, name='member_detail_with_barcode'),

    path('save-scheme/', save_scheme, name='save_scheme'),





]