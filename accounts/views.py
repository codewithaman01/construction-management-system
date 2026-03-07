# ✅ FIXED — accounts/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from core.models import RolePermission
from .models import User, Role


# ─────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Find default module
            permission = RolePermission.objects.filter(
                role=user.role,
                module__is_default=True
            ).first()

            # fallback module
            if not permission:
                permission = RolePermission.objects.filter(
                    role=user.role
                ).first()

            if permission:
                return redirect(permission.module.url)

            return redirect('/dashboard/')

        return render(request, 'login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'login.html')


# ─────────────────────────────────────────
# LOGOUT
# ─────────────────────────────────────────
@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


# ─────────────────────────────────────────
# REGISTER (New User)
# ─────────────────────────────────────────
def register_view(request):
    if request.method == 'POST':
        username  = request.POST.get('username')
        email     = request.POST.get('email')
        password  = request.POST.get('password')
        password2 = request.POST.get('password2')
        role_id   = request.POST.get('role')

        # Validation
        if password != password2:
            return render(request, 'register.html', {
                'error': 'Passwords do not match',
                'roles': Role.objects.all()
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username already taken',
                'roles': Role.objects.all()
            })

        # Create the user
        role = Role.objects.filter(id=role_id).first()
        user = User.objects.create_user(username=username, email=email, password=password)
        if role:
            user.role = role
            user.save()

        messages.success(request, 'Account created! Please log in.')
        return redirect('/')

    return render(request, 'register.html', {'roles': Role.objects.all()})


# ─────────────────────────────────────────
# FORGOT PASSWORD
# ─────────────────────────────────────────
def forgot_password_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()

        if user:
            # Generate a secure token
            token = default_token_generator.make_token(user)
            uid   = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"/accounts/reset-password/{uid}/{token}/"
            # In production: email this link. For now, show it on screen.
            return render(request, 'forgot_password.html', {
                'success': True,
                'reset_link': reset_link
            })

        return render(request, 'forgot_password.html', {'error': 'Username not found'})

    return render(request, 'forgot_password.html')


def reset_password_view(request, uidb64, token):
    try:
        uid  = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        return render(request, 'reset_password.html', {'error': 'Invalid link'})

    if not default_token_generator.check_token(user, token):
        return render(request, 'reset_password.html', {'error': 'Link expired or invalid'})

    if request.method == 'POST':
        p1 = request.POST.get('password')
        p2 = request.POST.get('password2')
        if p1 != p2:
            return render(request, 'reset_password.html', {'error': 'Passwords do not match'})
        user.set_password(p1)
        user.save()
        messages.success(request, 'Password reset! Please log in.')
        return redirect('/')

    return render(request, 'reset_password.html')


# ─────────────────────────────────────────
# API: list users (used by projects module)
# ─────────────────────────────────────────
@login_required                          # ← was missing, anyone could call this!
def get_users(request):
    users = User.objects.all().values('id', 'username')
    return JsonResponse({'users': list(users)})