from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'transaction_id',
        'amount',
        'status',
        'payment_date',
        'created_at',
    )

    search_fields = ('transaction_id', 'order__user__email')
    list_filter = ('status', 'created_at')