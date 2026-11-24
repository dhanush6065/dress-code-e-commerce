from django.contrib import admin
from .models import ProductReview


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'product',
        'rating',
        'status',
        'created_at',
    )
    list_editable = ('status',)

    list_filter = ('rating', 'status', 'created_at')

    search_fields = (
        'user__email',
        'product__name',
        'title',
        'comment',
    )