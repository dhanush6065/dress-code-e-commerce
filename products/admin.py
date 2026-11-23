from django.contrib import admin
from .models import Category ,Brand , Product , ProductVariant


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active',)    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'is_active')
    search_fields = ('name', 'brand__name', 'category__name')
    list_filter = ('category', 'brand', 'is_active')   

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'color', 'stock', 'additional_price', 'is_active')
    search_fields = ('product__name', 'size', 'color')
    list_filter = ('size', 'color', 'is_active')     