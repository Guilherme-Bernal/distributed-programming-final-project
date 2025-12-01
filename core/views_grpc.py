from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from backend_service.grpc_client import (
    enroll_student_grpc,
    unenroll_student_grpc,
    create_class_grpc,
    get_class_grpc,
    list_classes_grpc
)


@login_required
def enroll_class_grpc(request, pk):
    """Enroll student using gRPC"""
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Only students can enroll in classes.')
        return redirect('classes:detail', pk=pk)
    
    if request.method == 'POST':
        student = request.user.student_profile
        
        # Call gRPC service instead of direct service
        result = enroll_student_grpc(pk, student.id)
        
        if result['success']:
            messages.success(request, result['message'])
        else:
            messages.error(request, result['message'])
    
    return redirect('classes:detail', pk=pk)


@login_required
def unenroll_class_grpc(request, pk):
    """Unenroll student using gRPC"""
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Only students can unenroll from classes.')
        return redirect('classes:detail', pk=pk)
    
    if request.method == 'POST':
        student = request.user.student_profile
        
        # Call gRPC service
        result = unenroll_student_grpc(pk, student.id)
        
        if result['success']:
            messages.success(request, result['message'])
        else:
            messages.error(request, result['message'])
    
    return redirect('classes:detail', pk=pk)