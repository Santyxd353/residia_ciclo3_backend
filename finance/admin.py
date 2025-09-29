from django.contrib import admin
from .models import Expense, Payment

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('resident','period','amount','status','due_date','created_at')
    list_filter = ('status','period')
    search_fields = ('resident__user__email','resident__unit__house_number','period')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('expense','amount','method','ref_code','paid_at')
    search_fields = ('ref_code','expense__resident__user__email')
