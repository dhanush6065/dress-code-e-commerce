from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from orders.models import Order


def home(request):
    return render(request, 'adminpanel/index.html')


@staff_member_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'adminpanel/order_detail.html', {
        'order': order,
    })