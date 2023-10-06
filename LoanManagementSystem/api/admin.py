from django.contrib import admin

# Register your models here.
from .models import User,Transactions,Loan,EMI

class UserAdmin(admin.ModelAdmin):
    model = User

class TransactionAdmin(admin.ModelAdmin):
    model = Transactions

class LoanAdmin(admin.ModelAdmin):
    model = Loan

class EMIAdmin(admin.ModelAdmin):
    model = EMI

admin.site.register(Transactions,TransactionAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Loan,LoanAdmin)
admin.site.register(EMI,EMIAdmin)