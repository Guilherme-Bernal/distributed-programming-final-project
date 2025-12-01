from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from .models import Class, Subject
from accounts.models import Teacher, Student
from backend_service.services import EnrollmentService, ClassService, SubjectService


def class_list(request):
    """List all active classes with optional filtering"""
    classes = Class.objects.filter(is_active=True).select_related(
        'subject', 'teacher', 'teacher__user'
    ).prefetch_related('students')
    
    # Filter by semester
    semester = request.GET.get('semester')
    if semester:
        classes = classes.filter(semester=semester)
    
    # Filter by subject
    subject_id = request.GET.get('subject')
    if subject_id:
        classes = classes.filter(subject_id=subject_id)
    
    # Search
    search = request.GET.get('search')
    if search:
        classes = classes.filter(
            Q(subject__code__icontains=search) |
            Q(subject__name__icontains=search) |
            Q(teacher__user__first_name__icontains=search) |
            Q(teacher__user__last_name__icontains=search)
        )
    
    return render(request, 'classes/list.html', {
        'classes': classes,
        'current_semester': semester,
    })


def class_detail(request, pk):
    """Show class details"""
    class_obj = get_object_or_404(
        Class.objects.select_related('subject', 'teacher', 'teacher__user')
        .prefetch_related('students', 'students__user'),
        pk=pk
    )
    
    # Check if current user is enrolled (if student)
    is_enrolled = False
    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        is_enrolled = request.user.student_profile in class_obj.students.all()
    
    return render(request, 'classes/detail.html', {
        'class': class_obj,
        'is_enrolled': is_enrolled,
    })


@login_required
def class_create(request):
    """Create a new class"""
    # Only teachers and staff can create classes
    if not (hasattr(request.user, 'teacher_profile') or request.user.is_staff):
        messages.error(request, 'Only teachers can create classes.')
        return redirect('classes:list')
    
    subjects = Subject.objects.all().order_by('code')
    teachers = Teacher.objects.select_related('user').all()
    
    if request.method == 'POST':
        # Get form data
        subject_id = request.POST.get('subject')
        teacher_id = request.POST.get('teacher')
        schedule = request.POST.get('schedule')
        room = request.POST.get('room', '')
        semester = request.POST.get('semester')
        max_students = request.POST.get('max_students', 40)
        is_active = request.POST.get('is_active') == 'on'
        
        # If user is a teacher, use their profile
        if hasattr(request.user, 'teacher_profile') and not teacher_id:
            teacher_id = request.user.teacher_profile.id
        
        # Prepare data for service
        data = {
            'subject_id': subject_id,
            'teacher_id': teacher_id,
            'schedule': schedule,
            'room': room,
            'semester': semester,
            'max_students': max_students,
            'is_active': is_active,
        }
        
        # Use business logic service
        result = ClassService.create_class(data)
        
        if result['success']:
            messages.success(request, result['message'])
            return redirect('classes:detail', pk=result['class_id'])
        else:
            messages.error(request, result['message'])
    
    return render(request, 'classes/create.html', {
        'subjects': subjects,
        'teachers': teachers,
    })


@login_required
def class_edit(request, pk):
    """Edit an existing class"""
    class_obj = get_object_or_404(Class, pk=pk)
    
    # Only the teacher who owns the class or staff can edit
    if hasattr(request.user, 'teacher_profile'):
        if class_obj.teacher != request.user.teacher_profile and not request.user.is_staff:
            messages.error(request, 'You can only edit your own classes.')
            return redirect('classes:detail', pk=pk)
    elif not request.user.is_staff:
        messages.error(request, 'Only teachers can edit classes.')
        return redirect('classes:detail', pk=pk)
    
    if request.method == 'POST':
        # Update class
        class_obj.schedule = request.POST.get('schedule')
        class_obj.room = request.POST.get('room', '')
        class_obj.semester = request.POST.get('semester')
        class_obj.max_students = int(request.POST.get('max_students', 40))
        class_obj.is_active = request.POST.get('is_active') == 'on'
        
        try:
            class_obj.save()
            messages.success(request, 'Class updated successfully!')
            return redirect('classes:detail', pk=pk)
        except Exception as e:
            messages.error(request, f'Error updating class: {str(e)}')
    
    return render(request, 'classes/edit.html', {
        'class': class_obj,
    })


@login_required
def class_delete(request, pk):
    """Delete a class"""
    class_obj = get_object_or_404(Class, pk=pk)
    
    # Only the teacher who owns the class or staff can delete
    if hasattr(request.user, 'teacher_profile'):
        if class_obj.teacher != request.user.teacher_profile and not request.user.is_staff:
            messages.error(request, 'You can only delete your own classes.')
            return redirect('classes:detail', pk=pk)
    elif not request.user.is_staff:
        messages.error(request, 'Only teachers can delete classes.')
        return redirect('classes:detail', pk=pk)
    
    if request.method == 'POST':
        class_name = str(class_obj)
        class_obj.delete()
        messages.success(request, f'Class "{class_name}" deleted successfully!')
        return redirect('classes:list')
    
    return redirect('classes:detail', pk=pk)


@login_required
def enroll_class(request, pk):
    """Enroll student in a class"""
    # Only students can enroll
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Only students can enroll in classes.')
        return redirect('classes:detail', pk=pk)
    
    if request.method == 'POST':
        student = request.user.student_profile
        
        # Use business logic service
        result = EnrollmentService.enroll_student(pk, student.id)
        
        if result['success']:
            messages.success(request, result['message'])
        else:
            messages.error(request, result['message'])
    
    return redirect('classes:detail', pk=pk)


@login_required
def unenroll_class(request, pk):
    """Unenroll student from a class"""
    # Only students can unenroll
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Only students can unenroll from classes.')
        return redirect('classes:detail', pk=pk)
    
    if request.method == 'POST':
        student = request.user.student_profile
        
        # Use business logic service
        result = EnrollmentService.unenroll_student(pk, student.id)
        
        if result['success']:
            messages.success(request, result['message'])
        else:
            messages.error(request, result['message'])
    
    return redirect('classes:detail', pk=pk)


@login_required
def my_classes(request):
    """Show student's enrolled classes"""
    # Only students can view their enrolled classes
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'This page is only for students.')
        return redirect('classes:list')
    
    student = request.user.student_profile
    
    # Get enrolled classes
    enrolled_classes = student.enrolled_classes.filter(
        is_active=True
    ).select_related('subject', 'teacher', 'teacher__user')
    
    # Calculate total credits
    total_credits = enrolled_classes.aggregate(
        total=Sum('subject__credits')
    )['total'] or 0
    
    return render(request, 'classes/my_classes.html', {
        'enrolled_classes': enrolled_classes,
        'total_credits': total_credits,
    })


@login_required
def my_teaching(request):
    """Show teacher's classes"""
    # Only teachers can view their teaching schedule
    if not hasattr(request.user, 'teacher_profile'):
        messages.error(request, 'This page is only for teachers.')
        return redirect('classes:list')
    
    teacher = request.user.teacher_profile
    
    # Get teaching classes
    teaching_classes = teacher.classes.filter(
        is_active=True
    ).select_related('subject').prefetch_related('students')
    
    # Calculate total students
    total_students = sum(c.enrolled_count for c in teaching_classes)
    
    return render(request, 'classes/my_teaching.html', {
        'teaching_classes': teaching_classes,
        'total_students': total_students,
    })


def subject_list(request):
    """List all subjects"""
    subjects = Subject.objects.all().prefetch_related('classes').order_by('code')
    
    return render(request, 'classes/subject_list.html', {
        'subjects': subjects,
    })


@login_required
def subject_create(request):
    """Create a new subject"""
    # Only staff can create subjects
    if not request.user.is_staff:
        messages.error(request, 'Only administrators can create subjects.')
        return redirect('classes:subject_list')
    
    if request.method == 'POST':
        # Get form data
        code = request.POST.get('code')
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        credits = request.POST.get('credits')
        
        # Prepare data for service
        data = {
            'code': code,
            'name': name,
            'description': description,
            'credits': credits,
        }
        
        # Use business logic service
        result = SubjectService.create_subject(data)
        
        if result['success']:
            messages.success(request, result['message'])
            return redirect('classes:subject_list')
        else:
            messages.error(request, result['message'])
    
    return render(request, 'classes/subject_create.html', {})


def dashboard(request):
    """System dashboard with statistics"""
    
    # Total counts
    total_classes = Class.objects.filter(is_active=True).count()
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_subjects = Subject.objects.count()
    
    # Enrollments by semester
    enrollments = Class.objects.filter(is_active=True).values('semester').annotate(
        count=Count('students')
    ).order_by('-semester')
    enrollments_by_semester = {e['semester']: e['count'] for e in enrollments}
    
    # Popular classes (top 5 by enrollment)
    # Use 'student_count' instead of 'enrolled_count' to avoid property conflict
    popular_classes_qs = Class.objects.filter(is_active=True).annotate(
        student_count=Count('students')
    ).select_related('subject').order_by('-student_count')[:5]
    
    # Convert to list with custom structure
    popular_classes = []
    for c in popular_classes_qs:
        popular_classes.append({
            'pk': c.pk,
            'subject': c.subject,
            'max_students': c.max_students,
            'student_count': c.student_count,
        })
    
    # User-specific stats
    user_stats = {}
    if request.user.is_authenticated:
        if hasattr(request.user, 'student_profile'):
            student = request.user.student_profile
            user_stats = {
                'type': 'student',
                'enrolled_count': student.enrolled_classes.filter(is_active=True).count(),
                'total_credits': student.enrolled_classes.filter(is_active=True).aggregate(
                    total=Sum('subject__credits')
                )['total'] or 0,
            }
        elif hasattr(request.user, 'teacher_profile'):
            teacher = request.user.teacher_profile
            teaching_classes = teacher.classes.filter(is_active=True)
            user_stats = {
                'type': 'teacher',
                'teaching_count': teaching_classes.count(),
                'total_students': sum(c.enrolled_count for c in teaching_classes),
            }
    
    return render(request, 'classes/dashboard.html', {
        'total_classes': total_classes,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_subjects': total_subjects,
        'enrollments_by_semester': enrollments_by_semester,
        'popular_classes': popular_classes,
        'user_stats': user_stats,
    })