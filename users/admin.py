from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User , Address


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions')
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',
                       'is_staff', 'is_superuser', 'is_active'),
        }),
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'city', 'state', 'user', 'is_default')
    search_fields = ('full_name', 'phone', 'city', 'user__email')
    list_filter = ('state', 'is_default')    