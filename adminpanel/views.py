from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from orders.models import Order
from users.models import User
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.cache import never_cache

@never_cache
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff and request.user.is_active:
        return redirect('admin_home')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=email, password=password)

        if user is not None and user.is_staff and user.is_active:
            login(request, user)
            return redirect('admin_home')

        messages.error(request, 'Invalid email or password.')

    return render(request, 'adminpanel/admin_login.html')


@never_cache
@staff_member_required(login_url='/adminpanel/login/')
def home(request):
    return render(request, 'adminpanel/index.html')


@never_cache
@staff_member_required(login_url='/adminpanel/login/')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'adminpanel/order_detail.html', {
        'order': order,
    })


@never_cache
@staff_member_required(login_url='/adminpanel/login/')
def user_list(request):
    search_query = request.GET.get('search', '').strip()

    all_users = User.objects.all()

   
    total_users = all_users.count()
    active_users_count = all_users.filter(is_active=True).count()
    blocked_users_count = all_users.filter(is_active=False).count()

    now = timezone.now()
    month_start = now.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    new_users_count = all_users.filter(
        date_joined__gte=month_start
    ).count()

    
    users = all_users.order_by('-date_joined')

    
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
        'total_users': total_users,
        'active_users_count': active_users_count,
        'blocked_users_count': blocked_users_count,
        'new_users_count': new_users_count,
    })



@never_cache
@staff_member_required(login_url='/adminpanel/login/')
@require_POST
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Prevent blocking superusers
    if user.is_superuser:
        messages.error(request, 'Superusers cannot be blocked.')
        return redirect('user_list')

    user.is_active = not user.is_active
    user.save()

    return redirect('user_list')


@never_cache
@require_POST
def admin_logout(request):
    logout(request)
    return redirect('admin_login')
