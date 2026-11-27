from django.shortcuts import render


def product_detail(request):
    return render(request, 'products/product_detail.html')