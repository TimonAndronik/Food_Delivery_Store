from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_home')
            return redirect('user_home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_home')
            return redirect('user_home')
        messages.error(request, "Невірний логін або пароль")
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def user_home(request):
    if not request.user.is_authenticated or request.user.role != 'user':
        return redirect('login')
    return render(request, 'accounts/user_home.html')

def admin_home(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return redirect('login')
    return render(request, 'accounts/admin_home.html')
