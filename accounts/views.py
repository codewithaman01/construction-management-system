from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from core.models import RolePermission


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔥 FIRST: get default module
            permission = RolePermission.objects.filter(
                role=user.role,
                module__is_default=True
            ).select_related('module').first()

            # 🔁 If no default, fallback to any module
            if not permission:
                permission = RolePermission.objects.filter(
                    role=user.role
                ).select_related('module').first()

            if permission:
                return redirect(permission.module.url)

            return redirect('/')  # final fallback

        return render(request, 'login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'login.html')