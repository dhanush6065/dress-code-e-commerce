from django.contrib import admin
from .models import Offer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'product',
        'category',
        'discount_type',
        'discount_value',
        'start_date',
        'end_date',
        'is_active',
    )

    search_fields = ('name', 'product__name', 'category__name')
    list_filter = ('discount_type', 'is_active')