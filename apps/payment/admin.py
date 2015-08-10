from django.contrib import admin
from apps.payment.models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment_type', 'date']

admin.site.register(Payment, PaymentAdmin)