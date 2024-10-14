from django.db import models

class Member(models.Model):
    number = models.CharField(primary_key=True,max_length=50)
    name = models.CharField(max_length=100)
    group = models.CharField(max_length=10)
    scheme_name = models.CharField(max_length=50)
    scheme_id = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pin = models.CharField(max_length=15)
    phno1 = models.IntegerField()
    phno2 = models.IntegerField()
    aadhaar = models.CharField(max_length=50)
    pan = models.CharField(max_length=50)
    wt_conversion = models.CharField(max_length=50)
    metal = models.CharField(max_length=50)
    email = models.EmailField()
    installment = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    join_date = models.DateField(auto_now_add = True)
    #nominee
    nominee_name = models.CharField(max_length=50,null=True)
    nominee_email = models.EmailField(null=True)
    nominee_phone_no = models.CharField(max_length=50,null=True)
    nominee_dob = models.CharField(max_length=50,null=True)
    #referal
    referral_name = models.CharField(max_length=50,null=True)
    referral_number = models.CharField(max_length=50,null=True)