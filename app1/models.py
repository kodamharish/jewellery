from django.db import models
from django.contrib.auth.hashers import make_password
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


# class Member(models.Model):
#     id = models.CharField(primary_key=True,max_length=50)
#     created_by = models.ForeignKey(User,on_delete=models.CASCADE)
#     name = models.CharField(max_length=100,null=True)
#     group = models.CharField(max_length=10,null=True)
#     scheme_name = models.CharField(max_length=50,null=True)
#     scheme_id = models.CharField(max_length=10,null=True)
#     address = models.CharField(max_length=100,null=True)
#     city = models.CharField(max_length=100,null=True)
#     pin = models.CharField(max_length=15,null=True)
#     phno1 = models.IntegerField(null=True)
#     phno2 = models.IntegerField(null=True)
#     aadhaar = models.CharField(max_length=50,null=True)
#     pan = models.CharField(max_length=50,null=True)
#     wt_conversion = models.CharField(max_length=50,null=True)
#     metal = models.CharField(max_length=50,null=True)
#     email = models.EmailField(null=True)
#     installment = models.CharField(max_length=50,null=True)
#     status = models.CharField(max_length=50,null=True)
#     join_date = models.DateField(auto_now_add = True)
#     #nominee
#     nominee_name = models.CharField(max_length=50,null=True)
#     nominee_email = models.EmailField(null=True)
#     nominee_phone_no = models.CharField(max_length=50,null=True)
#     nominee_dob = models.CharField(max_length=50,null=True)
#     #referal
#     referral_name = models.CharField(max_length=50,null=True)
#     referral_number = models.CharField(max_length=50,null=True)
#     def __str__(self):
#         return self.id



class Member(models.Model):
    id = models.IntegerField(primary_key=True)  # Custom ID field
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    group = models.CharField(max_length=10, null=True)
    scheme_name = models.CharField(max_length=50, null=True)
    scheme_id = models.CharField(max_length=10, null=True)
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
    join_date = models.DateField(auto_now_add=True)
    # Nominee
    nominee_name = models.CharField(max_length=50, null=True)
    nominee_email = models.EmailField(null=True)
    nominee_phone_no = models.CharField(max_length=50, null=True)
    nominee_dob = models.CharField(max_length=50, null=True)
    # Referral
    referral_name = models.CharField(max_length=50, null=True)
    referral_number = models.CharField(max_length=50, null=True)

    def save(self, *args, **kwargs):
        # Auto-increment id if not set
        if not self.id:
            last_member = Member.objects.order_by('-id').first()
            if last_member:
                self.id = last_member.id + 1
            else:
                self.id = 1  # Start from 1

        super(Member, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)







from django.db import models

# class Scheme(models.Model):
#     scheme_id = models.PositiveIntegerField(primary_key=True)  # Custom ID field
#     scheme_name = models.CharField(max_length=100)

#     def save(self, *args, **kwargs):
#         # Auto-increment scheme_id if not set
#         if not self.scheme_id:
#             last_scheme = Scheme.objects.order_by('-scheme_id').first()
#             if last_scheme:
#                 self.scheme_id = last_scheme.scheme_id + 1
#             else:
#                 self.scheme_id = 1  # Start from 1

#         super(Scheme, self).save(*args, **kwargs)

#     def __str__(self):
#         return str(self.scheme_id)





# class Group(models.Model):
#     group_id = models.PositiveIntegerField(primary_key=True)  # Custom ID field
#     group_name = models.CharField(max_length=100)
#     scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)

#     def save(self, *args, **kwargs):
#         # Auto-increment group_id if not set
#         if not self.group_id:
#             last_group = Group.objects.order_by('-group_id').first()
#             if last_group:
#                 self.group_id = last_group.group_id + 1
#             else:
#                 self.group_id = 1  # Start from 1

#         super(Group, self).save(*args, **kwargs)

#     def __str__(self):
#         return str(self.group_id)


from django.db import models

class Scheme(models.Model):
    scheme_id = models.AutoField(primary_key=True)  # Auto-incremented ID field
    scheme_name = models.CharField(max_length=100)

    def __str__(self):
        return self.scheme_name


class Group(models.Model):
    group_id = models.AutoField(primary_key=True)  # Auto-incremented ID field
    group_name = models.CharField(max_length=100)
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)

    def __str__(self):
        return self.group_name



from django.db import models

class Transaction(models.Model):
    trasaction_id = models.IntegerField(unique=True, blank=True, null=True)  # Auto-increment from 1
    voucher_no = models.IntegerField(unique=True, blank=True, null=True)  # Auto-increment from 1
    
    transaction = models.CharField(max_length=50)

    receipt_date = models.DateField()
    receipt_time = models.TimeField(auto_now=True)
    receipt_amount = models.IntegerField()
    member_name = models.CharField(max_length=50)
    member_number = models.CharField(max_length=50)
    member_group = models.CharField(max_length=50)
    total_amount = models.IntegerField()
    payment_mode = models.CharField(max_length=50)
    remarks = models.CharField(max_length=50)
    ent_by = models.CharField(max_length=50)
    installment_in_grams = models.FloatField()
    

    def save(self, *args, **kwargs):
        # Auto-increment transaction_id if not set
        if not self.trasaction_id:
            last_transaction = Transaction.objects.order_by('-trasaction_id').first()
            if last_transaction:
                self.trasaction_id = last_transaction.trasaction_id + 1
            else:
                self.trasaction_id = 1  # Start from 1

        # Auto-increment voucher_no if not set
        if not self.voucher_no:
            last_voucher = Transaction.objects.order_by('-voucher_no').first()
            if last_voucher:
                self.voucher_no = last_voucher.voucher_no + 1
            else:
                self.voucher_no = 1  # Start from 1

        super(Transaction, self).save(*args, **kwargs)

    






# from django.db import models

# class Rate(models.Model):
#     id = models.PositiveIntegerField(primary_key=True)  # Custom ID field
#     purity = models.CharField(max_length=50)
#     rate_10_grams = models.IntegerField()
#     rate_1_gram = models.IntegerField()

#     def save(self, *args, **kwargs):
#         # Auto-increment id if not set
#         if not self.id:
#             last_rate = Rate.objects.order_by('-id').first()
#             if last_rate:
#                 self.id = last_rate.id + 1
#             else:
#                 self.id = 1  # Start from 1

#         super(Rate, self).save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.purity} - {self.rate_10_grams} per 10g"



    

from django.db import models

class Rate(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incremented ID field
    purity = models.CharField(max_length=50)
    rate_10_grams = models.IntegerField()
    rate_1_gram = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return str(self.id)




