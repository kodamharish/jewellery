from django.shortcuts import render,redirect
from django.contrib.auth.hashers import check_password
from .models import *
from django.contrib import messages
from django.db.models import Q
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.contrib import messages
import datetime
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import *
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# Get the current date
current_date = date.today()





# Create your views here.
def login1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #print(username,'username')
        user = User.objects.get(username=username)

        if user:
            # Check if the password is correct
            if check_password(password, user.password):
                print(user.username)
                request.session['current_user'] = user.username  # Save QC in session

            
                return redirect('dashboard')  # Redirect to a dashboard or home page
            else:
                messages.error(request,'Invalid username or password')
                return redirect('login')  # Redirect to a dashboard or home page
        else:
            messages.error(request,'Invalid username')
            
    else:
        return render(request,'login.html')
    



def login_old(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            
            # Check if the password is correct
            if check_password(password, user.password):
                print(user.username)
                request.session['current_user'] = user.username  # Save user in session
                return redirect('dashboard')  # Redirect to the dashboard or home page
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')

        except User.DoesNotExist:
            messages.error(request, 'Invalid username')
            return redirect('login')
        
    else:
        return render(request,'login.html')



from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from .models import User

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            
            # Check if the password is correct
            if check_password(password, user.password):
                request.session['current_user'] = user.username  # Save user in session
                return redirect('dashboard')  # Redirect to the dashboard or home page
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')

        except User.DoesNotExist:
            messages.error(request, 'Invalid username')
            return redirect('login')
        
    else:
        # If no current user, redirect to the login page
        if 'current_user' not in request.session:
            return render(request, 'login.html')
        else:
            return redirect('dashboard')

def dashboard_old(request):
    members = Member.objects.all()

    current_user = request.session['current_user']
    #print(current_user,'current_user')
    context= {'current_user':current_user,'members':members}

    return render(request,'dashboard.html',context)


def dashboard(request):
    # Safely get 'current_user' from the session
    current_user = request.session.get('current_user')

    if not current_user:
        # If there's no current user, redirect to the login page
        return redirect('login')

    members = Member.objects.all()
    context = {'current_user': current_user, 'members': members}

    return render(request, 'dashboard.html', context)

def installment_remainder_old(request):
    current_user = request.session['current_user']
    context= {'current_user':current_user}

    return render(request,'installment_remainder.html',context)


def member_details_old(request):
    if request.method == 'POST':
        pass
    else:
        status = request.GET.get('status')
        #print(status,'status')

        current_user = request.session['current_user']
        members = Member.objects.all()
        context= {'current_user':current_user,'members':members,'status':status}
        return render(request,'member_details.html',context)


def installment_remainder(request):
    # Safely get 'current_user' from the session
    current_user = request.session.get('current_user')

    if not current_user:
        # If there's no current user, redirect to the login page
        return redirect('login')

    context = {'current_user': current_user}
    return render(request, 'installment_remainder.html', context)


def member_details_old(request):
    # Safely get 'current_user' from the session
    current_user = request.session.get('current_user')

    if not current_user:
        # If there's no current user, redirect to the login page
        return redirect('login')
    
    search_query = request.GET.get('search', '')
    # current_gold_rate_1_gram = Rate.objects.filter(date=current_date).first()
    members = None

    # Perform the search
    if search_query:
        

        members = Member.objects.filter(
            Q(id__exact=search_query) |
            Q(phone_number__exact=search_query)
        ).all()

        if not members.exists():
            messages.error(request, 'No member found with that number or phone.')
            members = None

    if request.method == 'POST':
        # Handle POST request logic here
        pass
    else:
        #status = request.GET.get('status')
        members = Member.objects.all()
        context = {'current_user': current_user, 'members': members}
        return render(request, 'member_details.html', context)


def member_details_old2(request):
    # Safely get 'current_user' from the session
    current_user = request.session.get('current_user')

    if not current_user:
        # If there's no current user, redirect to the login page
        return redirect('login')
    
    search_query = request.GET.get('search', '')
    members = None

    # Perform the search if there's a search query
    if search_query:
        members = Member.objects.filter(
            Q(id__exact=search_query) |
            Q(phone_number__exact=search_query)
        )

        if not members.exists():
            messages.error(request, 'No member found with that number or phone.')
            members = Member.objects.all()
    else:
        # If there's no search query, get all members
        members = Member.objects.all()

    context = {'current_user': current_user, 'members': members}
    return render(request, 'member_details.html', context)

def member_details_old3(request):
    # Safely get 'current_user' from the session
    current_user = request.session.get('current_user')

    if not current_user:
        # If there's no current user, redirect to the login page
        return redirect('login')
    
    search_query = request.GET.get('search', '')
    members = None

    # Perform the search if there's a search query
    if search_query:
        members = Member.objects.filter(
            Q(id__exact=search_query) |
            Q(phone_number__exact=search_query)
        )

        if not members.exists():
            messages.error(request, 'No member found with that number or phone.')
            members = None
    else:
        # If there's no search query, do not fetch all members
        members = None

    context = {'current_user': current_user, 'members': members}
    return render(request, 'member_details.html', context)

def member_details(request):
    # Safely get 'current_user' from the session
    current_user = request.session.get('current_user')

    if not current_user:
        # If there's no current user, redirect to the login page
        return redirect('login')
    
    search_query = request.GET.get('search', '')
    
    if search_query:
        # Perform the search
        members = Member.objects.filter(
            Q(id__exact=search_query) |
            Q(phone_number__exact=search_query)
        )

        if not members.exists():
            messages.error(request, 'No member found with that number or phone.')
            members = None
    else:
        # Initially show all members
        members = Member.objects.all()

    context = {'current_user': current_user, 'members': members}
    return render(request, 'member_details.html', context)

def recepit_old(request):
    current_user = request.session.get('current_user')
    search_query = request.GET.get('search', '')
   
    current_gold_rate_1_gram = Rate.objects.filter(date=current_date).first()
    # print(current_gold_rate_1_gram.rate_1_gram)

    member = None

    # Perform the search
    if search_query:
        try:
            # Search by member number or phone number (phno1 or phno2)
            member = Member.objects.filter(
                Q(id__icontains=search_query) |
                Q(phone_number__icontains=search_query) 
            ).all()  
            if not member:
                messages.error(request, 'No member found with that number or phone.')
        except Member.DoesNotExist:
            messages.error(request, 'No member found.')  # Display an error message
            member = None  # Handle no results found

    if request.method == 'POST':
        date = request.POST.get('date')
        member_name = request.POST.get('member_name')
        recepit_amount = request.POST.get('recepit_amount')
        payment_mode = request.POST.get('payment_mode')
        member_id = request.POST.get('member_id')
        remark = request.POST.get('remark')
        ent_by = request.POST.get('ent_by')
        installment_in_grams = float(recepit_amount) / current_gold_rate_1_gram.rate_1_gram

        transaction = Transaction(
            receipt_date=date,
            member_name=member_name,
            member_id=member_id,
            receipt_amount=recepit_amount,
            payment_mode=payment_mode,
            transaction='receipt',
            remarks=remark,
            ent_by=ent_by,
            installment_in_grams=installment_in_grams
        )
        transaction.save()
        messages.success(request, 'Transaction Successful')
        return redirect('recepit')

    context = {
        'current_user': current_user,
        'member': member,  # Passing the member object to the template
        'current_date': current_date,  # Pass the current date
        'current_gold_rate_1_gram': current_gold_rate_1_gram
    }

    return render(request, 'recepit.html', context)


# Search by member number or phone number (phno1 or phno2)
        # member = Member.objects.filter(
        #     Q(id__icontains=search_query) |
        #     Q(phone_number__icontains=search_query) 
        # ).all()

def recepit(request):
    # Safely get 'current_user' from the session
    current_user = request.session.get('current_user')

    if not current_user:
        # If there's no current user, redirect to the login page
        return redirect('login')

    search_query = request.GET.get('search', '')
    current_gold_rate_1_gram = Rate.objects.filter(date=current_date).first()
    member = None

    # Perform the search
    if search_query:
        

        member = Member.objects.filter(
            Q(id__exact=search_query) |
            Q(phone_number__exact=search_query)
        ).all()

        if not member.exists():
            messages.error(request, 'No member found with that number or phone.')
            member = None

    if request.method == 'POST':
        pass

    context = {
        'current_user': current_user,
        'member': member,  # Passing the member object to the template
        'current_date': current_date,  # Pass the current date
        'current_gold_rate_1_gram': current_gold_rate_1_gram
    }

    return render(request, 'recepit.html', context)

def recepit_form_old(request,member_id,scheme_id):
    current_user = request.session.get('current_user')
    current_gold_rate_1_gram = Rate.objects.filter(date=current_date).first()
    

    if request.method == 'POST':
        date = request.POST.get('date')
        member_name = request.POST.get('member_name')
        recepit_amount = request.POST.get('recepit_amount')
        payment_mode = request.POST.get('payment_mode')
        member_id = request.POST.get('member_id')
        remark = request.POST.get('remark')
        ent_by = request.POST.get('ent_by')
        installment_in_grams = float(recepit_amount) / current_gold_rate_1_gram.rate_1_gram

        transaction = Transaction(
            receipt_date=date,
            member_name=member_name,
            member_id=member_id,
            receipt_amount=recepit_amount,
            payment_mode=payment_mode,
            transaction='receipt',
            remarks=remark,
            ent_by=ent_by,
            installment_in_grams=installment_in_grams
        )
        transaction.save()
        messages.success(request, 'Transaction Successful')
        return redirect('recepit_form')
    

    else:

        member = Member.objects.get(id=member_id)

        context = {
            'current_user': current_user,
            'member':member,
            
            'current_date': current_date,  # Pass the current date
            'current_gold_rate_1_gram': current_gold_rate_1_gram
        }

        return render(request, 'recepit_form.html', context)


def recepit_form(request,id):
    current_user = request.session.get('current_user')
    current_gold_rate_1_gram = Rate.objects.filter(date=current_date).first()
    member = Member.objects.get(id=id)
    

    if request.method == 'POST':
        date = request.POST.get('date')
        member_name = request.POST.get('member_name')
        scheme_name = request.POST.get('scheme_name')

        recepit_amount = request.POST.get('recepit_amount')
        payment_mode = request.POST.get('payment_mode')
        #member_id = request.POST.get('member_id')
        remark = request.POST.get('remark')
        ent_by = request.POST.get('ent_by')
        installment_in_grams = float(recepit_amount) / current_gold_rate_1_gram.rate_1_gram

        transaction = Transaction(
            receipt_date=date,
            member =member,
            scheme_name= scheme_name,
            receipt_amount=recepit_amount,
            payment_mode=payment_mode,
            transaction='receipt',
            remarks=remark,
            ent_by=ent_by,
            installment_in_grams=installment_in_grams
        )
        transaction.save()
        messages.success(request, 'Transaction Successful')
        return redirect('recepit_form',id)
    

    else:

        

        context = {
            'current_user': current_user,
            'member':member,
            
            'current_date': current_date,  # Pass the current date
            'current_gold_rate_1_gram': current_gold_rate_1_gram
        }

        return render(request, 'recepit_form.html', context)

import random
import string

def generate_referral_code(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))





def add_member_old(request):
    maturity_period_choices = Scheme.MATURITY_PERIOD_CHOICES
    benefit_choices = Scheme.BENEFIT_CHOICES

    if request.method == 'POST':
        # Extract form data as before
        memberName = request.POST.get('member_name')
        
        address = request.POST.get('address')
        city = request.POST.get('city')
        phone_number = request.POST.get('phone_number')
        aadhaar = request.POST.get('aadhaar')
        pan = request.POST.get('pan')
        pin = request.POST.get('pin')
        wtc = request.POST.get('wtc')
        metal = request.POST.get('metal')
        scheme_name = request.POST.get('scheme_name')
        referred_person_name = request.POST.get('referred_person_name')
        referred_person_id = request.POST.get('referred_person_id')
        email = request.POST.get('email')
        join_date = request.POST.get('join_date')  # This should be in the format 'YYYY-MM-DD'
        referred_person_referral_code = request.POST.get('referred_person_referral_code')

        current_user = request.session['current_user']
        user = User.objects.get(username=current_user)
        scheme = Scheme.objects.get(scheme_name=scheme_name)

        # Calculate the end_date based on the scheme_maturity_period
        scheme_maturity_period = int(scheme.scheme_maturity_period)
        join_date_obj = datetime.strptime(join_date, '%Y-%m-%d')
        end_date = join_date_obj + relativedelta(months=scheme_maturity_period)

        # Proceed with member creation
        member = Member(
            created_by=user,
            name=memberName,
            
            address=address,
            city=city,
            pin=pin,
            phone_number=phone_number,
            aadhaar=aadhaar,
            pan=pan,
            wt_conversion=wtc,
            metal=metal,
            email=email,
            installment=0,
            status='active',
            referred_person_name=referred_person_name,
            referred_person_id=referred_person_id,
            referred_person_referral_code=referred_person_referral_code,
            scheme=scheme,
            join_date=join_date,
            end_date=end_date.date()  # Save only the date part
        )
        member.save()
        messages.success(request, 'Member Created Successfully')
        return redirect('add_member')

    else:
        current_user = request.session['current_user']
        schemes = Scheme.objects.all()
        # Ensure that you use the scheme saved in the session if it's available
        
        
        #current_date = datetime.now().date()

        context = {
            'current_user': current_user,
            'schemes': schemes,
            'maturity_period_choices': maturity_period_choices,
            'benefit_choices': benefit_choices,
            'current_date': current_date,  # Pass the current date
            
        }

        return render(request, 'member_regform.html', context)




def add_member(request):
    maturity_period_choices = Scheme.MATURITY_PERIOD_CHOICES
    benefit_choices = Scheme.BENEFIT_CHOICES

    if request.method == 'POST':
        # Extract form data as before
        memberName = request.POST.get('member_name')
        
        address = request.POST.get('address')
        city = request.POST.get('city')
        phone_number = request.POST.get('phone_number')
        aadhaar = request.POST.get('aadhaar')
        pan = request.POST.get('pan')
        pin = request.POST.get('pin')
        
        scheme_name = request.POST.get('scheme_name')
        referred_person_name = request.POST.get('referred_person_name')
        referred_person_id = request.POST.get('referred_person_id')
        email = request.POST.get('email')
        join_date = request.POST.get('join_date')  # This should be in the format 'YYYY-MM-DD'
        referred_person_referral_code = request.POST.get('referred_person_referral_code')

        current_user = request.session['current_user']
        user = User.objects.get(username=current_user)
        scheme = Scheme.objects.get(scheme_name=scheme_name)

        # Calculate the end_date based on the scheme_maturity_period
        scheme_maturity_period = int(scheme.scheme_maturity_period)
        join_date_obj = datetime.strptime(join_date, '%Y-%m-%d')
        end_date = join_date_obj + relativedelta(months=scheme_maturity_period)

        # Proceed with member creation
        member = Member(
            created_by=user,
            name=memberName,
            address=address,
            city=city,
            pin=pin,
            phone_number=phone_number,
            aadhaar=aadhaar,
            pan=pan,
           
            email=email,
            status='active',
            referred_person_name=referred_person_name,
            referred_person_id=referred_person_id,
            referred_person_referral_code=referred_person_referral_code,
            scheme=scheme,
            join_date=join_date,
            end_date=end_date.date()  # Save only the date part
        )
        member.save()
        messages.success(request, 'Member Created Successfully')
        return redirect('add_member')

    else:
        current_user = request.session['current_user']
        schemes = Scheme.objects.all()
        current_date = datetime.now().date()

        context = {
            'current_user': current_user,
            'schemes': schemes,
            'maturity_period_choices': maturity_period_choices,
            'benefit_choices': benefit_choices,
            'current_date': current_date,  # Pass the current date
        }

        return render(request, 'member_regform.html', context)


def edit_member(request,id):
    maturity_period_choices = Scheme.MATURITY_PERIOD_CHOICES
    benefit_choices = Scheme.BENEFIT_CHOICES

    if request.method == 'POST':
        # Extract form data as before
        memberName = request.POST.get('member_name')
        
        address = request.POST.get('address')
        city = request.POST.get('city')
        phone_number = request.POST.get('phone_number')
        
        aadhaar = request.POST.get('aadhaar')
        pan = request.POST.get('pan')
        pin = request.POST.get('pin')
       
        scheme_name = request.POST.get('scheme_name')
        referred_person_name = request.POST.get('referred_person_name')
        referred_person_id = request.POST.get('referred_person_id')
        email = request.POST.get('email')
        join_date = request.POST.get('join_date')  # This should be in the format 'YYYY-MM-DD'
        referred_person_referral_code = request.POST.get('referred_person_referral_code')

        current_user = request.session['current_user']
        user = User.objects.get(username=current_user)
        scheme = Scheme.objects.get(scheme_name=scheme_name)

        nominee_name = request.POST.get('nominee_name')
        nominee_email = request.POST.get('nominee_email')
        nominee_phone_number = request.POST.get('nominee_phone_number')
        nominee_dob = request.POST.get('nominee_dob')
        nominee_adhaar = request.POST.get('nominee_adhaar')
        nominee_pan = request.POST.get('nominee_pan')
        
        member = Member.objects.get(id=id)
        member.name=memberName
        member.address=address
        member.city=city
        member.pin=pin
        member.phone_number=phone_number
        member.aadhaar=aadhaar
        member.pan=pan
        
        member.email=email
        member.nominee_name=nominee_name
        member.nominee_email=nominee_email
        member.nominee_phone_number=nominee_phone_number
        member.nominee_dob=nominee_dob
        member.nominee_adhaar=nominee_adhaar
        member.nominee_pan=nominee_pan

                                
        member.save()
        messages.success(request, 'Member Updated Successfully')
        return redirect('edit_member',id=id)

    else:
        current_user = request.session['current_user']
        schemes = Scheme.objects.all()
        #current_date = datetime.now().date()
        member = Member.objects.get(id=id)

        context = {
            'current_user': current_user,
            'schemes': schemes,
            'maturity_period_choices': maturity_period_choices,
            'benefit_choices': benefit_choices,
            'current_date': current_date,  # Pass the current date
            'member':member
        }

        return render(request, 'member_edit_form.html', context)



def add_nominee(request):
    if request.method == 'POST':
        nominee_name = request.POST.get('nominee_name')
        nominee_email = request.POST.get('nominee_email')
        nominee_phone_number = request.POST.get('nominee_phone_number')
        nominee_dob = request.POST.get('nominee_dob')
        nominee_adhaar = request.POST.get('nominee_adhaar')
        nominee_pan = request.POST.get('nominee_pan')


        member = Member.objects.latest('id')
        member.nominee_name = nominee_name
        member.nominee_email = nominee_email
        member.nominee_phone_no = nominee_phone_number
        member.nominee_dob = nominee_dob
        member.nominee_adhaar = nominee_adhaar
        member.nominee_pan = nominee_pan

        member.save()

        messages.success(request,'Nominee  Created Succesfully')
        return redirect('add_member')

    else:
        current_user = request.session['current_user']
        context= {'current_user':current_user}
        
        return render(request,'member_regform.html',context)





def add_scheme(request):
    if request.method == 'POST':
        
        scheme_name = request.POST.get('add_scheme_name')
        maturity_period = request.POST.get('add_scheme_maturity_period')
        benefit = request.POST.get('add_scheme_benefit')
        installment_amount = request.POST.get('add_scheme_installment_amount')

       
        scheme = Scheme(
            
            scheme_name = scheme_name,
            scheme_maturity_period = maturity_period,
            scheme_benefit = benefit,
            scheme_installment_amount = installment_amount
            #scheme_id = scheme_id

        )
        scheme.save()
        messages.success(request,'New Scheme Created Succesfully')
        return redirect('add_member')

    else:
        current_user = request.session['current_user']
        schemes = Scheme.objects.all()
        

        context= {'current_user':current_user,'schemes':schemes,}
        
        return render(request,'member_regform.html',context)





def scheme_refund_old1(request):

    # Safely get 'current_user' from the session
    current_user = request.session.get('current_user')

    if not current_user:
        # If there's no current user, redirect to the login page
        return redirect('login')

    search_query = request.GET.get('search', '')
    
    member = None

    # Perform the search
    if search_query:
        

        member = Transaction.objects.filter(
            Q(member__id__exact=search_query) |
            Q(memberphone_number__exact=search_query)
        ).all()

        if not member.exists():
            messages.error(request, 'No member found with that number or phone.')
            member = None

    if request.method == 'POST':
        pass

    context = {
        'current_user': current_user,
        'member': member,  # Passing the member object to the template
        'current_date': current_date,  # Pass the current date
        
    }

    return render(request,'scheme_refund.html',context)





def scheme_refund_old2(request):
    # Safely get 'current_user' from the session
    current_user = request.session.get('current_user')

    if not current_user:
        # If there's no current user, redirect to the login page
        return redirect('login')

    search_query = request.GET.get('search', '')
    
    transactions = None

    # Perform the search
    if search_query:
        # Filter transactions based on the member's phone number or member ID
        transactions = Transaction.objects.filter(
            Q(member__id__exact=search_query) |  # Search by phone number 1
            Q(member__phone_number__exact=search_query)    # Search by phone number 2
        ).all()

        if not transactions.exists():
            messages.error(request, 'No transaction found for that member phone number.')
            transactions = None
    

    context = {
        'current_user': current_user,
        'transactions': transactions,  # Pass the transactions to the template
        'current_date': current_date,  # Pass the current date
    }

    return render(request, 'scheme_refund.html', context)



def scheme_refund(request):
    # Safely get 'current_user' from the session
    current_user = request.session.get('current_user')

    if not current_user:
        # If there's no current user, redirect to the login page
        return redirect('login')

    search_query = request.GET.get('search', '')
    

    member = None

    # Perform the search
    if search_query:

        member = Member.objects.filter(
            Q(id__exact=search_query) |
            Q(phone_number__exact=search_query)
        ).all()

        if not member.exists():
            messages.error(request, 'No member found with that number or phone.')
            member = None

    if request.method == 'POST':
        pass

    context = {
        'current_user': current_user,
        'member': member,  # Passing the member object to the template
        'current_date': current_date,  # Pass the current date
        
    }

    return render(request, 'scheme_refund.html', context)




def transactions_old(request,id,scheme_name):
    # Safely get 'current_user' from the session
    current_user = request.session.get('current_user')

    if not current_user:
        # If there's no current user, redirect to the login page
        return redirect('login')

    
    transactions = None

    
    transactions = Transaction.objects.filter(
        Q(member__id__exact=id) |  # Search by phone number 1
        Q(scheme_name__exact=scheme_name)    # Search by phone number 2
    ).all()

    print(transactions)

    if not transactions.exists():
        messages.error(request, 'No transaction found for that member phone number.')
        transactions = None

    
    

    context = {
        'current_user': current_user,
        'transactions': transactions,  # Pass the transactions to the template
        'current_date': current_date,  # Pass the current date
    }

    return render(request, 'transactions.html', context)


from collections import defaultdict

def transactions(request, id, scheme_name):
    # Safely get 'current_user' from the session
    current_user = request.session.get('current_user')

    if not current_user:
        # If there's no current user, redirect to the login page
        return redirect('login')

    transactions = Transaction.objects.filter(
        Q(member__id__exact=id) |
        Q(scheme_name__exact=scheme_name)
    ).all()

    if not transactions.exists():
        messages.error(request, 'No transaction found for that member phone number.')
        transactions = None

    # Group transactions by member
    transactions_by_member = defaultdict(list)
    for transaction in transactions:
        transactions_by_member[transaction.member].append(transaction)

    context = {
        'current_user': current_user,
        'transactions_by_member': transactions_by_member.items(),  # Pass as list of (member, transactions)
    }

    return render(request, 'transactions.html', context)





def scheme_refund_form(request,id):
    current_user = request.session.get('current_user')
    
    if request.method == 'POST':
        refund_date = request.POST.get('refund_date')
        email = request.POST.get('email')
        maturity_period = request.POST.get('maturity_period')
        total_amount_received = request.POST.get('total_amount_received')
        scheme_name = request.POST.get('scheme_name')
        phone_number = request.POST.get('phone_number')
        refund_by = request.POST.get('refund_by')

        member = Member.objects.get(id=id)

        refund = Refund(
            date = refund_date,
            member = member,
            scheme_name = scheme_name,
            email =email,
            phone_number = phone_number,
            maturity_period = maturity_period,
            total_amount_received = total_amount_received,
            refund_by = refund_by,
            refund_amount = total_amount_received

        )
        refund.save()
        messages.success(request,'Amount Refund Sucessfully Completed')
        return redirect('scheme_refund_form',id=id)

    else:

        member = Member.objects.get(id=id)
        total_amount = member.total_amount()  # Call the method to get the total amount

        context = {
            'current_user': current_user,
            'member':member,
            'total_amount': total_amount,
            'current_date': current_date,  # Pass the current date
            
        }

        return render(request, 'scheme_refund_form.html', context)




def tag(request):
    return render(request,'tag.html')



def logout(request):
    request.session.flush()

    return redirect('login')






from django.shortcuts import render
from .models import Member

def member_detail_with_barcode(request, member_number):
    try:
        member = Member.objects.get(id=member_number)
    except Member.DoesNotExist:
        return HttpResponse("Member not found", status=404)
    
    # Pass the member object to the template
    context = {
        'member': member,
    }
    return render(request, 'member_detail.html', context)


from django.http import HttpResponse
from .models import Member
import barcode
from barcode.writer import ImageWriter
from io import BytesIO

def generate_member_barcode(request, member_id):
    try:
        member = Member.objects.get(id=member_id)
    except Member.DoesNotExist:
        return HttpResponse("Member not found", status=404)

    # Combine member details to include in the barcode
    #barcode_data = f"{member.id}|{member.group}|{member.name}|{member.phno1}"
    barcode_data = f"{member.id}|{member.name}"

    #barcode_data = f"{member.id}"


    # Generate barcode without human-readable text
    CODE128 = barcode.get_barcode_class('code128')
    
    # ImageWriter options to suppress the human-readable text
    writer = ImageWriter()
    writer_options = {
        'write_text': False,  # Suppress human-readable text
    }

    barcode_image = CODE128(barcode_data, writer=writer)

    # Save to a bytes buffer
    buffer = BytesIO()
    barcode_image.write(buffer, options=writer_options)

    # Return as PNG image
    response = HttpResponse(buffer.getvalue(), content_type="image/png")
    response['Content-Disposition'] = f'inline; filename={member.id}_barcode.png'
    
    return response



from django.http import HttpResponse
from .models import Member
import qrcode
from io import BytesIO

def generate_member_qrcode(request, member_id):
    try:
        member = Member.objects.get(id=member_id)
    except Member.DoesNotExist:
        return HttpResponse("Member not found", status=404)

    # Combine member details to include in the QR code
    qr_data = (
        f"ID: {member.id}\n"
        f"Name: {member.name}\n"
        f"Scheme: {member.scheme.scheme_name}"
        f"Phone: {member.phone_number}\n"
        f"Address: {member.address}\n"
        f"City: {member.city}\n"
        f"Aadhaar: {member.aadhaar}"
    )

    # Create a QR code object
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Generate the QR code image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save to a bytes buffer
    buffer = BytesIO()
    img.save(buffer, format="PNG")

    # Return as PNG image
    response = HttpResponse(buffer.getvalue(), content_type="image/png")
    response['Content-Disposition'] = f'inline; filename={member.id}_qrcode.png'
    
    return response



from barcode import get_barcode_class
from barcode.writer import ImageWriter
from io import BytesIO
from django.http import HttpResponse

def generate_member_barcode2(request, member_id):
    try:
        member = Member.objects.get(id=member_id)
    except Member.DoesNotExist:
        return HttpResponse("Member not found", status=404)

    barcode_data = f"{member.id}"

    # Get the CODE128 barcode class
    CODE128 = get_barcode_class('code128')
    if CODE128 is None:
        return HttpResponse("Barcode class not found", status=500)

    writer = ImageWriter()
    writer_options = {
        'write_text': False,  # Suppress human-readable text
    }

    # Generate the barcode
    barcode_image = CODE128(barcode_data, writer=writer)

    # Save to a bytes buffer
    buffer = BytesIO()
    barcode_image.write(buffer, options=writer_options)

    # Return as PNG image
    response = HttpResponse(buffer.getvalue(), content_type="image/png")
    response['Content-Disposition'] = f'inline; filename={member.id}_barcode.png'

    return response















