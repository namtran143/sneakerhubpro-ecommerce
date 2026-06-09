from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import LoginForm, ProfileForm, RegisterForm

def auth_view(request):
    tab = request.POST.get('tab') or request.GET.get('tab', 'login')
    login_form = LoginForm(request, data=request.POST if request.method == 'POST' and tab == 'login' else None)
    register_form = RegisterForm(request.POST if request.method == 'POST' and tab == 'register' else None)

    if request.method == 'POST':
        if tab == 'login' and login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, f'Xin chào {user.display_name}, bạn đã đăng nhập thành công.')
            if user.is_superuser:
                return redirect('/admin/')
            if user.is_seller:
                return redirect('seller:dashboard')
            return redirect('products:home')

        if tab == 'register' and register_form.is_valid():
            user = register_form.save()
            messages.success(request, 'Đăng ký thành công. Bạn có thể đăng nhập ngay.')
            return redirect(f"{request.path}?tab=login")

    return render(request, 'auth/auth.html', {
        'tab': tab,
        'login_form': login_form,
        'register_form': register_form,
    })

@login_required
def profile_view(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Cập nhật hồ sơ thành công.')
        return redirect('users:profile')
    return render(request, 'auth/profile.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Bạn đã đăng xuất khỏi hệ thống.')
    return redirect('users:auth')
