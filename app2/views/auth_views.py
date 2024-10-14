from django.shortcuts import render,redirect
from django.contrib.auth.hashers import check_password
from ..models.auth_models import User
from django.contrib import messages


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #print(username,'username')
        user = User.objects.get(username=username)
         # Check if the password is correct
        if check_password(password, user.password):
            print(user.username)
            request.session['current_user'] = user.username  # Save QC in session

           
            return redirect('dashboard')  # Redirect to a dashboard or home page
        else:
            messages.error(request,'Invalid username or password')
            return redirect('login')  # Redirect to a dashboard or home page

            
    else:
        return render(request,'login.html')
    








def logout(request):
    return redirect('login')




