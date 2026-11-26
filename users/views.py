from django.shortcuts import render
from django.shortcuts import render, redirect , get_object_or_404
from .forms import RegistrationForm , ProfileUpdateForm , AddressForm
import random
from datetime import timedelta

from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password , check_password
from django.utils import timezone

from .models import OTPVerification , User , Address
from django.contrib.auth import authenticate, login ,logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.cache import never_cache
# Create your views here.
def home(request):
    return render(request, 'users/index.html')

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            send_signup_otp(user)

            request.session['pending_user_id'] = user.id

            return redirect('verify_otp')

    else:
        form = RegistrationForm()

    return render(request, 'users/signup.html', {'form': form})

def verify_otp(request):
    user_id = request.session.get('pending_user_id')

    if not user_id:
        return redirect('signup')

    user = User.objects.filter(id=user_id).first()

    if not user:
        return redirect('signup')

    otp_record = OTPVerification.objects.filter(
        user=user,
        purpose='signup'
    ).order_by('-created_at').first()

    if not otp_record:
        return render(request, 'users/verify_otp.html', {
            'error': 'OTP not found. Please sign up again.'
        })

    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '')

        if otp_record.attempts >= 5:
            return render(request, 'users/verify_otp.html', {
                'error': 'Too many attempts. Please sign up again.'
            })

        otp_record.attempts += 1
        otp_record.save()

        if timezone.now() > otp_record.expires_at:
            return render(request, 'users/verify_otp.html', {
                'error': 'OTP has expired. Please sign up again.'
            })

        if check_password(entered_otp, otp_record.otp_hash):
            user.is_active = True
            user.save()

            otp_record.delete()
            request.session.pop('pending_user_id', None)

            return redirect('home')

        return render(request, 'users/verify_otp.html', {
            'error': 'Invalid OTP. Please try again.'
        })

    return render(request, 'users/verify_otp.html')


def customer_login(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'users/login.html', {
            'error': 'Invalid email or password.'
        })

    return render(request, 'users/login.html')


def generate_otp():
    return str(random.randint(100000, 999999))


def send_signup_otp(user, purpose='signup'):
    otp = generate_otp()

    OTPVerification.objects.filter(
        user=user,
        purpose=purpose
    ).delete()

    OTPVerification.objects.create(
        user=user,
        otp_hash=make_password(otp),
        purpose=purpose,
        expires_at=timezone.now() + timedelta(minutes=5)
    )

    send_mail(
        'Dress Code - Verification OTP',
        f'Your OTP is {otp}. It expires in 5 minutes.',
        None,
        [user.email],
        fail_silently=False,
    )
@require_POST
def customer_logout(request):
    logout(request)
    return redirect('home')   

def forgot_password(request):

    if request.method == 'POST':
        email = request.POST.get('email')

        user = User.objects.filter(
            email=email,
            is_active=True
        ).first()

        if user:
            send_signup_otp(user, purpose='password_reset')
            request.session['password_reset_user_id'] = user.id
            return redirect('reset_password_otp')

        return render(request, 'users/forgot_password.html', {
            'message': 'If the account exists, an OTP has been sent.'
        })

    return render(request, 'users/forgot_password.html') 

def reset_password_otp(request):

    user_id = request.session.get('password_reset_user_id')

    if not user_id:
        return redirect('forgot_password')

    user = User.objects.filter(id=user_id).first()

    if not user:
        return redirect('forgot_password')

    otp_record = OTPVerification.objects.filter(
        user=user,
        purpose='password_reset'
    ).order_by('-created_at').first()

    if not otp_record:
        return redirect('forgot_password')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '')

        if otp_record.attempts >= 5:
            return render(request, 'users/reset_password_otp.html', {
                'error': 'Too many attempts. Please request a new OTP.'
            })

        otp_record.attempts += 1
        otp_record.save()

        if timezone.now() > otp_record.expires_at:
            return render(request, 'users/reset_password_otp.html', {
                'error': 'OTP has expired. Please request a new OTP.'
            })

        if check_password(entered_otp, otp_record.otp_hash):
            request.session['password_reset_verified'] = True
            otp_record.delete()
            return redirect('set_new_password')

        return render(request, 'users/reset_password_otp.html', {
            'error': 'Invalid OTP. Please try again.'
        })

    return render(request, 'users/reset_password_otp.html')

@require_POST
def resend_password_reset_otp(request):
    user_id = request.session.get('password_reset_user_id')

    if not user_id:
        return redirect('forgot_password')

    user = User.objects.filter(id=user_id, is_active=True).first()

    if not user:
        return redirect('forgot_password')

    send_signup_otp(user, purpose='password_reset')

    return redirect('reset_password_otp')


def set_new_password(request):
    user_id = request.session.get('password_reset_user_id')
    verified = request.session.get('password_reset_verified')

    if not user_id or not verified:
        return redirect('forgot_password')

    user = User.objects.filter(id=user_id).first()

    if not user:
        return redirect('forgot_password')

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'users/set_new_password.html', {
                'error': 'Passwords do not match.'
            })

        user.set_password(password)
        user.save()

        request.session.pop('password_reset_user_id', None)
        request.session.pop('password_reset_verified', None)

        return redirect('login')

    return render(request, 'users/set_new_password.html')

@never_cache
@login_required
def customer_profile(request):
    return render(request, 'users/profile.html')
@never_cache
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {
        'form': form
    })
@never_cache
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'users/change_password.html', {
        'form': form
    })

@never_cache
@login_required
def change_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('email', '').strip().lower()

        if User.objects.filter(email__iexact=new_email).exists():
            return render(request, 'users/change_email.html', {
                'error': 'This email is already registered.'
            })

        if not new_email:
            return render(request, 'users/change_email.html', {
                'error': 'Email is required.'
            })

        otp = str(random.randint(100000, 999999))

        OTPVerification.objects.filter(
            user=request.user,
            purpose='email_change'
        ).delete()

        OTPVerification.objects.create(
            user=request.user,
            otp_hash=make_password(otp),
            purpose='email_change',
            expires_at=timezone.now() + timedelta(minutes=5)
        )

        request.session['new_email'] = new_email

        send_mail(
            'Email Change Verification OTP',
            f'Your OTP for changing your email is {otp}. It expires in 5 minutes.',
            None,
            [new_email],
        )

        return redirect('verify_new_email')

    return render(request, 'users/change_email.html')

@never_cache
@login_required
def verify_new_email(request):
    new_email = request.session.get('new_email')

    if not new_email:
        return redirect('change_email')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '')

        otp_record = OTPVerification.objects.filter(
            user=request.user,
            purpose='email_change'
        ).last()

        if not otp_record:
            return render(request, 'users/verify_new_email.html', {
                'error': 'OTP not found. Please request a new OTP.'
            })

        if otp_record.expires_at < timezone.now():
            return render(request, 'users/verify_new_email.html', {
                'error': 'OTP expired. Please request a new OTP.'
            })

        if otp_record.attempts >= 5:
            return render(request, 'users/verify_new_email.html', {
                'error': 'Too many attempts. Please request a new OTP.'
            })

        otp_record.attempts += 1
        otp_record.save()

        if check_password(entered_otp, otp_record.otp_hash):
            request.user.email = new_email
            request.user.save()

            otp_record.delete()
            request.session.pop('new_email', None)

            return redirect('profile')

        return render(request, 'users/verify_new_email.html', {
            'error': 'Invalid OTP. Please try again.'
        })

    return render(request, 'users/verify_new_email.html')



@require_POST
def resend_signup_otp(request):
    user_id = request.session.get('pending_user_id')

    if not user_id:
        return redirect('signup')

    user = User.objects.filter(id=user_id, is_active=False).first()

    if not user:
        return redirect('signup')

    send_signup_otp(user)

    return redirect('verify_otp')

@never_cache
@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)

        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()

            return redirect('profile')
    else:
        form = AddressForm()

    return render(request, 'users/add_address.html', {
        'form': form
    })

@never_cache
@login_required
def edit_address(request, address_id):
    address = get_object_or_404(
        Address,
        id=address_id,
        user=request.user
    )

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)

        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = AddressForm(instance=address)

    return render(request, 'users/edit_address.html', {
        'form': form
    })


@never_cache
@login_required
@require_POST
def delete_address(request, address_id):
    address = get_object_or_404(
        Address,
        id=address_id,
        user=request.user
    )

    address.delete()

    return redirect('profile')

@never_cache
@login_required
@require_POST
def set_default_address(request, address_id):
    address = get_object_or_404(
        Address,
        id=address_id,
        user=request.user
    )

    Address.objects.filter(user=request.user).update(is_default=False)

    address.is_default = True
    address.save()

    return redirect('profile')