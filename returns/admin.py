from django.contrib import admin
from .models import ReturnRequest


@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_item', 'user', 'status', 'requested_at')
    list_filter = ('status', 'requested_at')
    search_fields = ('user__email', 'reason')