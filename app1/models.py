from django.db import models
from django.contrib.auth.hashers import make_password
import random
import string
from datetime import date
from datetime import date
from django.db.models import Sum
from decimal import Decimal



def generate_referral_code():
    # Function to generate unique referral code
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# User Model
class User(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


# Scheme Model
class Scheme(models.Model):
    MATURITY_PERIOD_CHOICES = [(str(i), str(i)) for i in range(1, 37)]

    BENEFIT_CHOICES = [
        ('No wastage - No Making charges', 'No wastage - No Making charges'),
    ]

    scheme_id = models.AutoField(primary_key=True)
    scheme_name = models.CharField(max_length=100, unique=True)
    scheme_maturity_period = models.CharField(max_length=50, choices=MATURITY_PERIOD_CHOICES)
    scheme_benefit = models.CharField(max_length=50, choices=BENEFIT_CHOICES)
    scheme_installment_amount = models.CharField(max_length=50)

    def __str__(self):
        return self.scheme_name



    

from django.db import models
from django.db.models import Sum
from datetime import date
from decimal import Decimal

from django.utils import timezone
from datetime import timedelta






class Member(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    scheme = models.ForeignKey('Scheme', on_delete=models.CASCADE)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    pin = models.CharField(max_length=15, null=True)
    phone_number = models.IntegerField(null=True)
    aadhaar = models.CharField(max_length=50, null=True)
    pan = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
    status = models.CharField(max_length=50, null=True)
    join_date = models.DateField()
    end_date = models.DateField()
    nominee_name = models.CharField(max_length=50, null=True)
    nominee_email = models.EmailField(null=True)
    nominee_phone_number = models.IntegerField(null=True)
    nominee_aadhaar = models.CharField(max_length=50, null=True)
    nominee_pan = models.CharField(max_length=50, null=True)
    referred_person_name = models.CharField(max_length=50, null=True)
    referred_person_id = models.CharField(max_length=50, null=True)
    referred_person_referral_code = models.CharField(max_length=50, null=True)
    member_referral_code = models.CharField(max_length=8, unique=True, null=True)
    referral_points = models.IntegerField(default=0)
    total_paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pending_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_installments = models.IntegerField(default=0)
    due_installments = models.IntegerField(default=0)

    def _generate_unique_referral_code(self):
        code = generate_referral_code()
        while Member.objects.filter(member_referral_code=code).exists():
            code = generate_referral_code()
        return code

    def calculate_total_paid_amount(self):
        # Sum all receipt amounts linked to this member
        return Decimal(Transaction.objects.filter(member=self).aggregate(total=Sum('receipt_amount'))['total'] or 0)

    def calculate_paid_installments(self):
        installment_amount = Decimal(self.scheme.scheme_installment_amount)
        return int(self.total_paid_amount // installment_amount) if installment_amount > 0 else 0

    def calculate_due_installments(self):
        total_installments = int(self.scheme.scheme_maturity_period)
        return total_installments - self.paid_installments

    def calculate_pending_amount(self):
        installment_amount = Decimal(self.scheme.scheme_installment_amount)
        return self.due_installments * installment_amount

    def update_financials(self):
        """Updates the member's financial fields after a transaction."""
        self.total_paid_amount = self.calculate_total_paid_amount()
        self.paid_installments = self.calculate_paid_installments()
        self.due_installments = self.calculate_due_installments()
        self.pending_amount = self.calculate_pending_amount()
        self.save()

    def __str__(self):
        return f"{self.name} ({self.id})"

# Transaction Model
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    voucher_no = models.IntegerField(unique=True, blank=True, null=True)
    transaction = models.CharField(max_length=50)
    receipt_date = models.DateField()
    receipt_time = models.TimeField(auto_now=True)
    receipt_amount = models.DecimalField(max_digits=10, decimal_places=2)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    scheme_name = models.CharField(max_length=50)
    payment_mode = models.CharField(max_length=50)
    remarks = models.CharField(max_length=50)
    ent_by = models.CharField(max_length=50)
    installment_in_grams = models.DecimalField(max_digits=10, decimal_places=3)

    # Tracking monthly installment
    installment_month = models.IntegerField()
    installment_year = models.IntegerField()
    #paid_on_time = models.BooleanField(default=True)  # Field to track if payment was made on time

    def save(self, *args, **kwargs):
        if self.voucher_no is None:
            max_voucher_no = Transaction.objects.aggregate(models.Max('voucher_no'))['voucher_no__max']
            self.voucher_no = (max_voucher_no or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Transaction {self.transaction_id} for {self.member}'


# Refund Model
class Refund(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    scheme_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.IntegerField()
    maturity_period = models.DateField()
    total_amount_received = models.IntegerField()
    refund_amount = models.IntegerField()
    refund_by = models.CharField(max_length=100)

    # Link to the transaction being refunded
    #related_transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.id)


# Rate Model for storing gold rates
class Rate(models.Model):
    id = models.AutoField(primary_key=True)
    purity = models.CharField(max_length=50)
    rate_10_grams = models.IntegerField()
    rate_1_gram = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return str(self.id)


