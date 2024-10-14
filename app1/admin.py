from django.contrib import admin
from .models import User,Transaction,Member,Scheme,Group
from .models import *

# Register your models here.
#admin.site.register(User)
#admin.site.register(Transaction)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username','full_name','email')
    
admin.site.register(User, UserAdmin)



class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'group', 'address', 'city', 'phno1', 'email', 'installment', 'status', 'join_date')
    readonly_fields = ('join_date',)

admin.site.register(Member, MemberAdmin)



class TransactionAdmin(admin.ModelAdmin):
    list_display = ('trasaction_id','voucher_no','member_name','member_number')
    readonly_fields = ('receipt_time',)

admin.site.register(Transaction, TransactionAdmin)



class SchemeAdmin(admin.ModelAdmin):
    list_display = ('scheme_id','scheme_name')
    
admin.site.register(Scheme, SchemeAdmin)



class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_id','group_name','scheme')
    
admin.site.register(Group,GroupAdmin)

class RateAdmin(admin.ModelAdmin):
    list_display = ('id','purity')
    
admin.site.register(Rate,RateAdmin)
#username : admin
#password : 12345