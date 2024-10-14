from django.contrib import admin
from .models.auth_models import User
from .models.user_models import Member


# Register your models here.


# Register your models here.
admin.site.register(User)
#admin.site.register(Transaction)





class MemberAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'group', 'address', 'city', 'phno1', 'email', 'installment', 'status', 'join_date')
    readonly_fields = ('join_date',)

admin.site.register(Member, MemberAdmin)




#username : admin
#password : 12345