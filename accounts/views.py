from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from accounts.models import Student, Teacher


def register(request):
    """User registration - placeholder for now"""
    if request.method == 'POST':
        # This is a placeholder - in production, use Django forms
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        user_type = request.POST.get('user_type', 'student')
        
        # Basic validation
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'accounts/register.html')
        
        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            
            # Create profile based on type
            if user_type == 'teacher':
                user.is_staff = True
                user.save()
                # Teacher profile created by signal
            # Student profile created by signal
            
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('accounts:login')
            
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
    
    return render(request, 'accounts/register.html')


@login_required
def profile(request):
    """View user profile"""
    return render(request, 'accounts/profile.html')


@login_required
def profile_edit(request):
    """Edit user profile"""
    if request.method == 'POST':
        # Update basic user info
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        # Update profile info
        phone_number = request.POST.get('phone_number', '')
        
        if hasattr(request.user, 'student_profile'):
            request.user.student_profile.phone_number = phone_number
            request.user.student_profile.save()
        elif hasattr(request.user, 'teacher_profile'):
            request.user.teacher_profile.phone_number = phone_number
            request.user.teacher_profile.bio = request.POST.get('bio', '')
            request.user.teacher_profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/profile_edit.html')