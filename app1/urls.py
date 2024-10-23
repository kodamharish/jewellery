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
    path('recepit_form/<int:id>/',recepit_form,name="recepit_form"),
    #path('recepit_form/<int:member_id>/<int:scheme_id>/',recepit_form,name="recepit_form"),


    path('add_member',add_member,name="add_member"),
    path('edit_member/<int:id>/',edit_member,name="edit_member"),
    path('delete_member/<int:id>/',delete_member,name="delete_member"),


    path('add_scheme',add_scheme,name="add_scheme"),
    path('scheme_refund/',scheme_refund,name="scheme_refund"),
    path('scheme_refund_form/<int:id>/',scheme_refund_form,name="scheme_refund_form"),
    path('transactions/<int:id>/<str:scheme_name>/',transactions,name="transactions"),


    path('add_nominee',add_nominee,name="add_nominee"),
    path('tag',tag,name="tag"),
    
    
    path('member/<str:member_id>/qrcode', generate_member_qrcode, name='generate_member_qrcode'),

    



]