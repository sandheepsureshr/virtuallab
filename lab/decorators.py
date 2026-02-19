from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            messages.error(request, 'Admin access required.')
            return redirect('dashboard')
        return f(request, *args, **kwargs)
    return decorated_function


def student_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if hasattr(request.user, 'profile') and request.user.profile.is_blocked:
            messages.error(request, 'Your account has been blocked. Contact admin.')
            return redirect('login')
        return f(request, *args, **kwargs)
    return decorated_function
