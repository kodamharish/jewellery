from django.contrib import admin

from .models import *

# Register your models here.
#admin.site.register(User)
#admin.site.register(Transaction)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username','full_name','email')
    
admin.site.register(User, UserAdmin)



class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'join_date','end_date', 'scheme','phone_number', 'email', 'status','member_referral_code' )
    

admin.site.register(Member, MemberAdmin)



class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction','voucher_no','member')
    readonly_fields = ('receipt_time',)

admin.site.register(Transaction, TransactionAdmin)



class SchemeAdmin(admin.ModelAdmin):
    list_display = ('scheme_id','scheme_name')
    
admin.site.register(Scheme, SchemeAdmin)


class RefundAdmin(admin.ModelAdmin):
    list_display = ('id','member','scheme_name')
    
admin.site.register(Refund,RefundAdmin)


class RateAdmin(admin.ModelAdmin):
    list_display = ('id','purity')
    
admin.site.register(Rate,RateAdmin)




    

#username : admin
#password : 12345