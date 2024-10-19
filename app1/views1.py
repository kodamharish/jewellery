from django.shortcuts import render,redirect
from django.contrib.auth.hashers import check_password
from .models import *
from django.contrib import messages
from django.db.models import Q



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
    



def login(request):
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


def dashboard(request):
    members = Member.objects.all()

    current_user = request.session['current_user']
    #print(current_user,'current_user')
    context= {'current_user':current_user,'members':members}

    return render(request,'dashboard.html',context)



def installment_remainder(request):
    current_user = request.session['current_user']
    context= {'current_user':current_user}

    return render(request,'installment_remainder.html',context)


def member_details(request):
    if request.method == 'POST':
        pass
    else:
        status = request.GET.get('status')
        #print(status,'status')

        current_user = request.session['current_user']
        members = Member.objects.all()
        context= {'current_user':current_user,'members':members,'status':status}
        return render(request,'member_details.html',context)




from django.contrib import messages
import datetime


 # Get the current date
current_date = datetime.date.today()

def recepit(request):
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
                Q(phno1__icontains=search_query) |
                Q(phno2__icontains=search_query)
            ).first()  # Get the first match
            if not member:
                messages.error(request, 'No member found with that number or phone.')
        except Member.DoesNotExist:
            messages.error(request, 'No member found.')  # Display an error message
            member = None  # Handle no results found

    if request.method == 'POST':
        date = request.POST.get('date')
        member_name = request.POST.get('member_name')
        group = request.POST.get('group')
        total_amount = request.POST.get('total_amount')
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
            member_group=group,
            receipt_amount=recepit_amount,
            total_amount=total_amount,
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





import random
import string

def generate_referral_code(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))



def add_member(request):
    maturity_period_choices = Scheme.MATURITY_PERIOD_CHOICES
    benefit_choices = Scheme.BENEFIT_CHOICES
    if request.method == 'POST':
        # Extract form data as you're doing
        # ...
        memberName = request.POST.get('member_name')
        memberGroup = request.POST.get('member_group')
        address = request.POST.get('address')
        city = request.POST.get('city')
        phoneNo1 = request.POST.get('phone_number1')
        phoneNo2 = request.POST.get('phone_number2')
        aadhaar = request.POST.get('aadhaar')
        pan = request.POST.get('pan')
        pin = request.POST.get('pin')
        wtc = request.POST.get('wtc')
        metal = request.POST.get('metal')
        scheme_name = request.POST.get('scheme_name')
        scheme_id = request.POST.get('scheme_id')
        referred_person_name = request.POST.get('referred_person_name')
        referred_person_id = request.POST.get('referred_person_id')
        email = request.POST.get('email')
        join_date = request.POST.get('join_date')
        referred_person_referral_code = request.POST.get('referred_person_referral_code')

        current_user = request.session['current_user']
        user = User.objects.get(username=current_user)

        # Ensure that you use the scheme saved in the session if it's available
        scheme_name = request.session.get('selected_scheme_id', request.POST.get('scheme_name'))


        # Proceed with member creation
        member = Member(
            created_by=user,
            name=memberName,
            group=memberGroup,
            address=address,
            city=city,
            pin=pin,
            phno1=phoneNo1,
            phno2=phoneNo2,
            aadhaar=aadhaar,
            pan=pan,
            wt_conversion=wtc,
            metal=metal,
            email=email,
            installment=0,
            status='active',
            referred_person_name=referred_person_name,
            referred_person_id=referred_person_id,
            referred_person_referral_code = referred_person_referral_code,
            scheme_name=scheme_name,
            scheme_id=scheme_id,
            join_date = join_date
            
        )
        member.save()
        messages.success(request, 'Member Created Successfully')
        return redirect('add_member')

    else:
        current_user = request.session['current_user']
        schemes = Scheme.objects.all()
        groups = Group.objects.all()

        # Safely access 'selected_scheme_id' from the session
        selected_scheme_id = request.session.get('selected_scheme_id', None)

        context = {
            'current_user': current_user,
            'schemes': schemes,
            'groups': groups,
            'selected_scheme_id': selected_scheme_id,
            'maturity_period_choices': maturity_period_choices,
            'benefit_choices': benefit_choices,
             'current_date': current_date,  # Pass the current date

        }

        return render(request, 'member_regform.html', context)


def add_nominee(request):
    if request.method == 'POST':
        nominee_name = request.POST.get('nominee_name')
        nominee_email = request.POST.get('nominee_email')
        phone_number = request.POST.get('phone_number')
        dob = request.POST.get('dob')
        staff_p = request.POST.get('staff_p')
        pay = request.POST.get('pay')
        route = request.POST.get('route')
        payf = request.POST.get('payf')
        status = request.POST.get('status')
        exst_mem = request.POST.get('exst_mem')

        member = Member.objects.latest('number')
        member.nominee_name = nominee_name
        member.nominee_email = nominee_email
        member.nominee_phone_no = phone_number
        member.nominee_dob = dob
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
        groups = Group.objects.all()

        context= {'current_user':current_user,'schemes':schemes,'groups':groups}
        
        return render(request,'member_regform.html',context)




def add_group(request):
    if request.method == 'POST':
        
        #group_id = request.POST.get('add_group_id')
        group_name = request.POST.get('add_group_name')
        add_group_scheme_name = request.POST.get('add_group_scheme_name')
        #add_group_scheme_id = request.POST.get('add_group_scheme_id')

        scheme = Scheme.objects.get(scheme_name=add_group_scheme_name)
       
        group = Group(
            
            #group_id = group_id,
            group_name = group_name,
            scheme = scheme,
            #scheme_id = add_group_scheme_id

        )
        group.save()
        messages.success(request,'New Group Created Succesfully')
        return redirect('add_member')

    else:
        current_user = request.session['current_user']
        schemes = Scheme.objects.all()
        groups = Group.objects.all()
        


        context= {'current_user':current_user,'schemes':schemes,'groups':groups}
        
        return render(request,'member_regform.html',context)






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
        f"Scheme: {member.scheme_name}"
        f"Group: {member.group}\n"
        f"Phone 1: {member.phno1}\n"
        f"Phone 2: {member.phno2}\n"
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


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json




from django.http import JsonResponse

def save_scheme(request):
    if request.method == 'GET':
        scheme_id = request.GET.get('scheme_id')
        if scheme_id:
            # Save the scheme ID in the session
            request.session['selected_scheme_id'] = scheme_id
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'message': 'Invalid scheme ID'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

