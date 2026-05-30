from urllib import request

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserRegistrationForm, UserLoginForm
from orders.models import Order



def error_404_view(request, exception):
    return render(request, '404.html')


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('menu:home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('accounts:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('menu:home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('menu:home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('menu:home')


@login_required(login_url='accounts:login')
def profile(request):
    """User profile view"""
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    context = {
        'user': request.user,
        'orders': orders,
        'total_orders': orders.count(),
    }
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='accounts:login')
def change_password(request):
    """View for users to change their password"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'accounts/change_password.html', {
        'form': form
    })

from orders.models import Order

def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    total_orders = orders.count()
    recent_orders = orders[:5]  # last 5 orders
    return render(request, 'accounts/profile.html', {
        'orders': orders,
        'total_orders': total_orders,
        'recent_orders': recent_orders,
    })

