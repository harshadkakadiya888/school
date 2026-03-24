from django.contrib import admin
from .models import Fees, FeePayment


@admin.register(Fees)
class FeesAdmin(admin.ModelAdmin):
    list_display = ['student', 'total_fees', 'student_discount']

    def student_discount(self, obj):
        return obj.student.discount
    student_discount.short_description = 'Discount'


@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'amount', 'date']