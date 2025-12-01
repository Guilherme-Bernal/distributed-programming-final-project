from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def register(request):
    """Placeholder for registration - will implement later"""
    return render(request, 'accounts/register.html', {})

@login_required
def profile(request):
    """Placeholder for profile view - will implement later"""
    return render(request, 'accounts/profile.html', {})

@login_required
def profile_edit(request):
    """Placeholder for profile edit - will implement later"""
    return render(request, 'accounts/profile_edit.html', {})