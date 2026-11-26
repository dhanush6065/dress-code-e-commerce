from django.shortcuts import render, get_object_or_404 , redirect
from django.contrib.admin.views.decorators import staff_member_required
from orders.models import Order
from users.models import User
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.contrib.auth import logout

@staff_member_required
def home(request):
    return render(request, 'adminpanel/index.html')


@staff_member_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'adminpanel/order_detail.html', {
        'order': order,
    })

@staff_member_required
def user_list(request):
    search_query = request.GET.get('search', '')

    users = User.objects.all().order_by('-date_joined')

    if search_query:
        users = users.filter(
            email__icontains=search_query
        ) | users.filter(
            first_name__icontains=search_query
        ) | users.filter(
            last_name__icontains=search_query
        )

    paginator = Paginator(users, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'adminpanel/user_list.html', {
    'users': page_obj,
    'page_obj': page_obj,
    'search_query': search_query,
})

@staff_member_required
@require_POST
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user.is_superuser:
        return redirect('user_list')

    user.is_active = not user.is_active
    user.save()

    return redirect('user_list')


@staff_member_required
@require_POST
def admin_logout(request):
    logout(request)
    return redirect('admin:login')