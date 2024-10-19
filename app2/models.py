from django.db import models
from django.contrib.auth.hashers import make_password
import random
import string
#Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100,primary_key=True)
    password = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    #last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.IntegerField()


    def save(self, *args, **kwargs):
        # Hash the password before saving
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Scheme(models.Model):
    # MATURITY_PERIOD_CHOICES = [
    #     ('12 months', '12 months'),
    #     ('16 months', '16 months'),
    #     ('20 months', '20 months'),
    # ]

    #MATURITY_PERIOD_CHOICES = [(f"{i} month{'s' if i > 1 else ''}", f"{i} month{'s' if i > 1 else ''}") for i in range(1, 37)]
    MATURITY_PERIOD_CHOICES = [(str(i), str(i)) for i in range(1, 37)]

    BENEFIT_CHOICES = [
        ('No wastage - No Making charges', 'No wastage - No Making charges'),
    ]

    scheme_id = models.AutoField(primary_key=True)  # Auto-incremented ID field
    scheme_name = models.CharField(max_length=100)
    scheme_maturity_period = models.CharField(max_length=50, choices=MATURITY_PERIOD_CHOICES)
    scheme_benefit = models.CharField(max_length=50, choices=BENEFIT_CHOICES)
    scheme_installment_amount = models.CharField(max_length=50)

    def __str__(self):
        return self.scheme_name





# class Group(models.Model):
#     group_id = models.AutoField(primary_key=True)  # Auto-incremented ID field
#     group_name = models.CharField(max_length=100)
#     scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.group_name




def generate_referral_code(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

class Member(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    #group = models.CharField(max_length=10, null=True)
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    pin = models.CharField(max_length=15, null=True)
    phno1 = models.IntegerField(null=True)
    phno2 = models.IntegerField(null=True)
    aadhaar = models.CharField(max_length=50, null=True)
    pan = models.CharField(max_length=50, null=True)
    wt_conversion = models.CharField(max_length=50, null=True)
    metal = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
    installment = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)
    join_date = models.DateField()
    end_date = models.DateField()
    # Nominee
    nominee_name = models.CharField(max_length=50, null=True)
    nominee_email = models.EmailField(null=True)
    nominee_phone_no = models.CharField(max_length=50, null=True)
    nominee_dob = models.CharField(max_length=50, null=True)
    # Referral
    referred_person_name = models.CharField(max_length=50, null=True)
    referred_person_id = models.CharField(max_length=50, null=True)
    referred_person_referral_code = models.CharField(max_length=50, null=True)  # New field for referred person's code
    member_referral_code = models.CharField(max_length=8, unique=True, null=True)  # New field for member's generated code

    def save(self, *args, **kwargs):
        if not self.member_referral_code:
            self.member_referral_code = self._generate_unique_referral_code()
        super().save(*args, **kwargs)
    
    def _generate_unique_referral_code(self):
        code = generate_referral_code()
        while Member.objects.filter(member_referral_code=code).exists():
            code = generate_referral_code()
        return code

    def __str__(self):
        return str(self.id)





class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)  # Auto-incremented primary key
    voucher_no = models.IntegerField(unique=True, blank=True, null=True)  # Manually managed auto-increment field

    transaction = models.CharField(max_length=50)
    receipt_date = models.DateField()
    receipt_time = models.TimeField(auto_now=True)
    receipt_amount = models.IntegerField()
    member_name = models.CharField(max_length=50)
    member_id = models.CharField(max_length=50)
    member_group = models.CharField(max_length=50)
    total_amount = models.IntegerField()
    payment_mode = models.CharField(max_length=50)
    remarks = models.CharField(max_length=50)
    ent_by = models.CharField(max_length=50)
    installment_in_grams = models.DecimalField(max_digits=10, decimal_places=3)

    def save(self, *args, **kwargs):
        if self.voucher_no is None:  # Only set voucher_no if it's not already set
            # Get the maximum value of voucher_no from existing records
            max_voucher_no = Transaction.objects.aggregate(models.Max('voucher_no'))['voucher_no__max']
            self.voucher_no = (max_voucher_no or 0) + 1  # Increment by 1
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.transaction_id)








    

from django.db import models

class Rate(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incremented ID field
    purity = models.CharField(max_length=50)
    rate_10_grams = models.IntegerField()
    rate_1_gram = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return str(self.id)




