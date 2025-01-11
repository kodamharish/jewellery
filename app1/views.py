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



def dashboard1(request):
    # Safely get 'current_user' from the session
    current_user = request.session.get('current_user')

    if not current_user:
        # If there's no current user, redirect to the login page
        return redirect('login')

    members = Member.objects.all()
    
    context = {'current_user': current_user, 'members': members}

    return render(request, 'dashboard.html', context)



def dashboard2(request):
    # Safely get 'current_user' from the session
    current_user = request.session.get('current_user')

    if not current_user:
        # If there's no current user, redirect to the login page
        return redirect('login')

    members = Member.objects.all()
    member_transactions = []

    for member in members:
        # Get the latest transaction (i.e., last paid date) for the member
        latest_transaction = Transaction.objects.filter(member=member).order_by('-receipt_date').first()
        last_paid_date = latest_transaction.receipt_date if latest_transaction else None

        # Append member and their latest transaction to the list
        member_transactions.append({
            'member': member,
            'latest_transaction': latest_transaction,
            'last_paid_date': last_paid_date,
        })

    context = {
        'current_user': current_user,
        'member': member_transactions,
    }

    return render(request, 'dashboard.html', context)




from django.db.models import Max, F
from datetime import date

def dashboard3(request):
    # Safely get 'current_user' from the session
    current_user = request.session.get('current_user')

    if not current_user:
        # If there's no current user, redirect to the login page
        return redirect('login')

    members = Member.objects.all()

    member_data = []
    for member in members:
        # Get the latest transaction (i.e., last paid date) for the member
        latest_transaction = Transaction.objects.filter(member=member).order_by('-receipt_date').first()
        
        last_paid_date = latest_transaction.receipt_date if latest_transaction else None
        due_amt = 0

        if last_paid_date:
            # Calculate how many months are left until the scheme's maturity period
            maturity_period = int(member.scheme.scheme_maturity_period)
            months_paid = (last_paid_date.year - member.join_date.year) * 12 + last_paid_date.month - member.join_date.month
            months_due = maturity_period - months_paid

            # Calculate the due amount if months_due is positive
            if months_due > 0:
                due_amt = months_due * int(member.scheme.scheme_installment_amount)
        
        member_data.append({
            'id': member.id,
            'name': member.name,
            'phone_number': member.phone_number,
            'last_paid_date': last_paid_date,
            'due_amt': due_amt,
            'scheme_name':member.scheme.scheme_name,
            'latest_transaction':latest_transaction
            
            
        })

    context = {
        'current_user': current_user,
        'members': member_data
    }

    return render(request, 'dashboard.html', context)






from django.shortcuts import render, redirect
from datetime import date, timedelta
from decimal import Decimal
from django.db.models import Sum
from .models import Member, Transaction

def calculate_total_amount1(member):
    """Calculate the total amount paid by the member."""
    return Decimal(Transaction.objects.filter(member=member).aggregate(total=Sum('receipt_amount'))['total'] or 0)


def calculate_paid_installments1(member):
    """Calculate the total number of installments paid by the member."""
    total_paid_amount = calculate_total_amount(member)
    installment_amount = Decimal(member.scheme.scheme_installment_amount)  # Ensure this is a Decimal
    if installment_amount > 0:
        return total_paid_amount // installment_amount
    return 0


def calculate_due_installments1(member):
    """Calculate the number of due installments."""
    total_installments = int(member.scheme.scheme_maturity_period)  # Total installments based on scheme
    paid_installments_count = calculate_paid_installments(member)
    return total_installments - paid_installments_count


def is_payment_due_this_month1(member):
    """Check if payment is due for the current month."""
    today = date.today()

    # Check if the member has paid for this month
    current_month = today.month
    current_year = today.year

    # Find if there's a transaction for this month and year
    payment_this_month = Transaction.objects.filter(
        member=member, 
        installment_month=current_month, 
        installment_year=current_year
    ).exists()

    if not payment_this_month:
        return True  # Payment is due if no transaction exists for this month

    return False


def dashboard4(request):
    current_user = request.session.get('current_user')
    if not current_user:
        return redirect('login')

    members = Member.objects.all()

    # Initialize an empty list to store members and their calculated values
    members_data = []

    for member in members:
        try:
            total_paid_installments = calculate_paid_installments(member)
            due_installments = calculate_due_installments(member)
            is_payment_due_val = is_payment_due_this_month(member)  # Updated to check payment for the current month
        except Exception as e:
            # Handle any potential issues (e.g., missing data)
            total_paid_installments = 0
            due_installments = 0
            is_payment_due_val = False

        # Add all values to the members_data list
        members_data.append({
            'member': member,
            'total_paid_installments': total_paid_installments,
            'due_installments': due_installments,
            'is_payment_due': is_payment_due_val,
        })
    print(members_data,'members_data')

    context = {
        'current_user': current_user,
        'members_data': members_data,  # Pass the data list to the context
    }

    return render(request, 'dashboard.html', context)






from django.shortcuts import render, redirect
from datetime import date
from decimal import Decimal
from django.db.models import Sum
from .models import Member, Transaction

def calculate_total_amount(member):
    """Calculate the total amount paid by the member."""
    return Decimal(Transaction.objects.filter(member=member).aggregate(total=Sum('receipt_amount'))['total'] or 0)


def calculate_paid_installments(member):
    """Calculate the total number of installments paid by the member."""
    total_paid_amount = calculate_total_amount(member)
    installment_amount = Decimal(member.scheme.scheme_installment_amount)  # Ensure this is a Decimal
    if installment_amount > 0:
        return total_paid_amount // installment_amount
    return 0


def calculate_due_installments(member):
    """Calculate the number of due installments."""
    total_installments = int(member.scheme.scheme_maturity_period)  # Total installments based on scheme
    paid_installments_count = calculate_paid_installments(member)
    return total_installments - paid_installments_count


def get_current_month_transaction(member):
    """Retrieve the latest transaction for the current month and year."""
    today = date.today()
    current_month = today.month
    current_year = today.year

    # Query the latest transaction for the current month and year
    return Transaction.objects.filter(
        member=member, 
        installment_month=current_month, 
        installment_year=current_year
    ).order_by('-receipt_date').first()


def is_payment_due_this_month(member):
    """Check if payment is due for the current month."""
    transaction = get_current_month_transaction(member)
    if transaction:
        return False  # No payment is due if a transaction exists for the current month
    return True






def dashboard(request):
    current_user = request.session.get('current_user')
    if not current_user:
        return redirect('login')

    members = Member.objects.all()

    # Initialize an empty list to store members and their calculated values
    members_data = []

    for member in members:
        try:
            total_paid_installments = calculate_paid_installments(member)
            due_installments = calculate_due_installments(member)
            is_payment_due_val = is_payment_due_this_month(member)  # Updated to check payment for the current month

            # Fetch the current month's transaction details
            current_month_transaction = get_current_month_transaction(member)

            # If a transaction exists, capture the date and amount
            receipt_date = current_month_transaction.receipt_date if current_month_transaction else None
            receipt_amount = current_month_transaction.receipt_amount if current_month_transaction else 0

        except Exception as e:
            # Handle any potential issues (e.g., missing data)
            total_paid_installments = 0
            due_installments = 0
            is_payment_due_val = False
            receipt_date = None
            receipt_amount = 0

        # Add all values to the members_data list
        members_data.append({
            'member': member,
            'total_paid_installments': total_paid_installments,
            'due_installments': due_installments,
            'is_payment_due': is_payment_due_val,
            'receipt_date': receipt_date,
            'receipt_amount': receipt_amount,
        })

    context = {
        'current_user': current_user,
        'members_data': members_data,  # Pass the data list to the context
    }

    return render(request, 'dashboard.html', context)






def installment_remainder(request):
    # Safely get 'current_user' from the session
    current_user = request.session.get('current_user')

    if not current_user:
        # If there's no current user, redirect to the login page
        return redirect('login')

    context = {'current_user': current_user}
    return render(request, 'installment_remainder.html', context)









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




def recepit1(request):
    # Safely get 'current_user' from the session
    current_user = request.session.get('current_user')

    if not current_user:
        # If there's no current user, redirect to the login page
        return redirect('login')

    search_query = request.GET.get('search', '')
    current_gold_rate_1_gram = Rate.objects.filter(date=date.today()).first()
    member = None
    error_message = None  # Initialize error_message

    # Perform the search
    if search_query:
        member = Member.objects.filter(
            Q(id__exact=search_query) |
            Q(phone_number__exact=search_query)
        ).all()

        if not member.exists():
            error_message = 'No member found with that number or phone.'  # Set the error message
            member = None

    if request.method == 'POST':
        pass

    context = {
        'current_user': current_user,
        'member': member,  # Passing the member object to the template
        'current_date': date.today(),  # Pass the current date
        'current_gold_rate_1_gram': current_gold_rate_1_gram,
        'error_message': error_message,  # Pass the error message to the template
    }

    return render(request, 'recepit.html', context)

def recepit_form_old(request,id):
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



from django.utils.dateparse import parse_date

def recepit_form(request, id):
    current_user = request.session.get('current_user')
    current_date = date.today()  # Set current date
    current_gold_rate_1_gram = Rate.objects.filter(date=current_date).first()
    member = Member.objects.get(id=id)

    if request.method == 'POST':
        date_str = request.POST.get('date')  # Receipt date from the form (string)
        receipt_date = parse_date(date_str)  # Convert string to date object
        member_name = request.POST.get('member_name')
        scheme_name = request.POST.get('scheme_name')
        recepit_amount = request.POST.get('recepit_amount')
        payment_mode = request.POST.get('payment_mode')
        remark = request.POST.get('remark')
        ent_by = request.POST.get('ent_by')

        # Calculate installment in grams
        installment_in_grams = float(recepit_amount) / current_gold_rate_1_gram.rate_1_gram

        # Extract month and year from receipt_date
        installment_month = receipt_date.month
        installment_year = receipt_date.year

        # Create and save the transaction
        transaction = Transaction(
            receipt_date=receipt_date,
            member=member,
            scheme_name=scheme_name,
            receipt_amount=recepit_amount,
            payment_mode=payment_mode,
            transaction='receipt',
            remarks=remark,
            ent_by=ent_by,
            installment_in_grams=installment_in_grams,
            installment_month=installment_month,  # Save month
            installment_year=installment_year  # Save year
        )
        transaction.save()

        messages.success(request, 'Transaction Successful')
        return redirect('recepit_form', id)

    else:
        context = {
            'current_user': current_user,
            'member': member,
            'current_date': current_date,  # Pass the current date
            'current_gold_rate_1_gram': current_gold_rate_1_gram
        }

        return render(request, 'recepit_form.html', context)

import random
import string

def generate_referral_code(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


















def add_member1(request):
    maturity_period_choices = Scheme.MATURITY_PERIOD_CHOICES
    benefit_choices = Scheme.BENEFIT_CHOICES

    if request.method == 'POST':
        # Extract form data
        member_name = request.POST.get('member_name')
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
        join_date = request.POST.get('join_date')  # Should be in 'YYYY-MM-DD' format
        referred_person_referral_code = request.POST.get('referred_person_referral_code')




        
        #nominee details

        nominee_name = request.POST.get('nominee_name')
        nominee_email = request.POST.get('nominee_email')
        nominee_phone_number = request.POST.get('nominee_phone_number')
        nominee_dob = request.POST.get('nominee_dob')
        nominee_aadhaar = request.POST.get('nominee_aadhaar')
        nominee_pan = request.POST.get('nominee_pan')


        current_user = request.session['current_user']
        user = User.objects.get(username=current_user)
        scheme = Scheme.objects.get(scheme_name=scheme_name)

        # Calculate the end_date based on the scheme_maturity_period
        scheme_maturity_period = int(scheme.scheme_maturity_period)
        join_date_obj = datetime.strptime(join_date, '%Y-%m-%d')
        end_date = join_date_obj + relativedelta(months=scheme_maturity_period)

        # Check if a referral code is provided and handle referral points
        if referred_person_referral_code:
             
            try:
                referring_member = Member.objects.get(member_referral_code=referred_person_referral_code)
                # Add 10 points to the referring member for successful referral
                referring_member.add_referral_points(10)
                
                
                referring_member.save()
            except Member.DoesNotExist:
                messages.error(request, 'Invalid referral code. No referral points added.')
                return redirect('add_member')  # Redirect back if referral code is invalid

        # Proceed with member creation if no referral code issue
        member = Member(
            created_by=user,
            name=member_name,
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
            end_date=end_date.date(),  # Save only the date part

            nominee_name = nominee_name,
            nominee_email = nominee_email,
            nominee_phone_number = nominee_phone_number,
            nominee_dob = nominee_dob,
            nominee_aadhaar = nominee_aadhaar,
            nominee_pan = nominee_pan


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








def add_member12(request):
    maturity_period_choices = Scheme.MATURITY_PERIOD_CHOICES
    benefit_choices = Scheme.BENEFIT_CHOICES

    if request.method == 'POST':
        # Extract form data
        member_name = request.POST.get('member_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        phone_number = request.POST.get('phone_number')
        aadhaar = request.POST.get('aadhaar')
        pan = request.POST.get('pan')
        pin = request.POST.get('pin')
        scheme_name = request.POST.get('scheme_name')
        email = request.POST.get('email')
        join_date = request.POST.get('join_date')  # Should be in 'YYYY-MM-DD' format
        referred_person_referral_code = request.POST.get('referred_person_referral_code')

        # Nominee details
        nominee_name = request.POST.get('nominee_name')
        nominee_email = request.POST.get('nominee_email')
        nominee_phone_number = request.POST.get('nominee_phone_number')
        
        nominee_aadhaar = request.POST.get('nominee_aadhaar')
        nominee_pan = request.POST.get('nominee_pan')

        current_user = request.session['current_user']
        user = User.objects.get(username=current_user)
        scheme = Scheme.objects.get(scheme_name=scheme_name)

        # Calculate the end_date based on the scheme_maturity_period
        scheme_maturity_period = int(scheme.scheme_maturity_period)
        join_date_obj = datetime.strptime(join_date, '%Y-%m-%d')
        end_date = join_date_obj + relativedelta(months=scheme_maturity_period)

        referred_person_id = None
        # Initialize referring_member
        referring_member = None

        # Check if a referral code is provided and handle referral points
        if referred_person_referral_code:
            try:
                referring_member = Member.objects.get(member_referral_code=referred_person_referral_code)
                referred_person_id = referring_member.id  # Get the referred person's ID
                # Add 10 points to the referring member for successful referral
                referring_member.add_referral_points(10)
                referring_member.save()
            except Member.DoesNotExist:
                messages.error(request, 'Invalid referral code. No referral points added.')
                return redirect('add_member')  # Redirect back if referral code is invalid

        # Proceed with member creation if no referral code issue
        member = Member(
            created_by=user,
            name=member_name,
            address=address,
            city=city,
            pin=pin,
            phone_number=phone_number,
            aadhaar=aadhaar,
            pan=pan,
            email=email,
            status='active',
            referred_person_name=referring_member.name if referring_member else None,
            referred_person_id=referred_person_id,  # Save the referred person's ID
            referred_person_referral_code=referred_person_referral_code,
            scheme=scheme,
            join_date=join_date,
            end_date=end_date.date(),  # Save only the date part

            nominee_name=nominee_name,
            nominee_email=nominee_email,
            nominee_phone_number=nominee_phone_number,
            nominee_aadhaar=nominee_aadhaar,
            nominee_pan=nominee_pan
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

def add_member(request):
    maturity_period_choices = Scheme.MATURITY_PERIOD_CHOICES
    benefit_choices = Scheme.BENEFIT_CHOICES

    if request.method == 'POST':
        # Extract form data
        member_name = request.POST.get('member_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        phone_number = request.POST.get('phone_number')
        aadhaar = request.POST.get('aadhaar')
        pan = request.POST.get('pan')
        pin = request.POST.get('pin')
        scheme_name = request.POST.get('scheme_name')
        email = request.POST.get('email')
        join_date = request.POST.get('join_date')
        referred_person_referral_code = request.POST.get('referred_person_referral_code')

        # Nominee details
        nominee_name = request.POST.get('nominee_name')
        nominee_email = request.POST.get('nominee_email')
        nominee_phone_number = request.POST.get('nominee_phone_number')
        nominee_aadhaar = request.POST.get('nominee_aadhaar')
        nominee_pan = request.POST.get('nominee_pan')

        current_user = request.session['current_user']
        user = User.objects.get(username=current_user)
        scheme = Scheme.objects.get(scheme_name=scheme_name)

        # Calculate the end_date based on the scheme_maturity_period
        scheme_maturity_period = int(scheme.scheme_maturity_period)
        join_date_obj = datetime.strptime(join_date, '%Y-%m-%d')
        end_date = join_date_obj + relativedelta(months=scheme_maturity_period)

        # Initialize optional referral fields
        referring_member = None
        referred_person_id = None
        referred_person_name = None
        referred_person_referral_code = None

        # Handle referral code if provided
        if referred_person_referral_code:
            try:
                referring_member = Member.objects.get(member_referral_code=referred_person_referral_code)
                referred_person_id = referring_member.id
                referred_person_name = referring_member.name
                referred_person_referral_code = referring_member.member_referral_code
                referring_member.add_referral_points(10)
                referring_member.save()
            except Member.DoesNotExist:
                messages.error(request, 'Invalid referral code. No referral points added.')
                return redirect('add_member')

        # Proceed with member creation
        member = Member(
            created_by=user,
            name=member_name,
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
            end_date=end_date.date(),
            nominee_name=nominee_name,
            nominee_email=nominee_email,
            nominee_phone_number=nominee_phone_number,
            nominee_aadhaar=nominee_aadhaar,
            nominee_pan=nominee_pan
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
            'current_date': current_date,
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
        
        nominee_aadhaar = request.POST.get('nominee_aadhaar')
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

        member.nominee_aadhaar=nominee_aadhaar
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



def delete_member(request,id):
    member = Member.objects.get(id=id)
    member.delete()
    messages.success(request,'member deleted succesfully')
    return redirect('member_details')

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
            return redirect('scheme_refund')


    if request.method == 'POST':
        pass

    context = {
        'current_user': current_user,
        'member': member,  # Passing the member object to the template
        'current_date': current_date,  # Pass the current date
        
    }

    return render(request, 'scheme_refund.html', context)







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
        return redirect('scheme_refund')

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







def new(request):
    return render(request,'new.html')







#APIs



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .models import Member, Scheme
from .serializers import *

class AddMemberAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        # Ensure the scheme exists
        try:
            scheme = Scheme.objects.get(scheme_id=data.get('scheme_id'))
        except Scheme.DoesNotExist:
            return Response(
                {"scheme_id": ["Invalid scheme_id. Object does not exist."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Parse and validate join_date
        try:
            join_date = datetime.strptime(data.get('join_date'), '%Y-%m-%d').date()
        except (TypeError, ValueError):
            return Response(
                {"join_date": ["Invalid date format. Use YYYY-MM-DD."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate end_date based on scheme maturity period
        scheme_maturity_period = int(scheme.scheme_maturity_period)
        end_date = join_date + relativedelta(months=scheme_maturity_period)

        # Prepare the data for the serializer
        serializer_data = {
            **data,
            "scheme": scheme.scheme_id,
            "created_by": "harish",
            "end_date": end_date
        }

        serializer = MemberSerializer(data=serializer_data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Member created successfully!", "member": serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Scheme
from .serializers import SchemeSerializer

class SchemeListAPIView(APIView):
    def get(self, request):
        """
        Fetch all scheme details.
        """
        schemes = Scheme.objects.all()
        serializer = SchemeSerializer(schemes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MemberListAPIView(APIView):
    def get(self, request):
        """
        Fetch all member details.
        """
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)