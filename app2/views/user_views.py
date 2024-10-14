from django.shortcuts import render,redirect
from django.contrib.auth.hashers import check_password
from ..models.auth_models import User
from ..models.user_models import Member

from django.contrib import messages

def dashboard(request):
    members = Member.objects.all()

    current_user = request.session['current_user']
    #print(current_user,'current_user')
    context= {'current_user':current_user,'members':members}

    return render(request,'dashboard.html',context)