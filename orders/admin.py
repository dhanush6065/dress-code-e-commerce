from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'status',
        'payment_method',
        'payment_status',
        'total_amount',
        'created_at',
    )
    search_fields = ('user__email',)
    list_filter = ('status', 'payment_method', 'payment_status')
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_variant', 'quantity', 'price')
    search_fields = ('order__user__email', 'product_variant__product__name')