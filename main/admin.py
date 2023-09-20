from django.contrib import admin

from main.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'course', 'lesson', 'amount', 'method')
