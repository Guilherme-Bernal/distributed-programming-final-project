from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Student, Teacher


class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'Student Profile'
    fk_name = 'user'


class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False
    verbose_name_plural = 'Teacher Profile'
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    inlines = (StudentInline, TeacherInline)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_user_type')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    
    def get_user_type(self, obj):
        if hasattr(obj, 'student_profile'):
            return '🎓 Student'
        elif hasattr(obj, 'teacher_profile'):
            return '👨‍🏫 Teacher'
        elif obj.is_superuser:
            return '👑 Admin'
        return '❓ Unknown'
    get_user_type.short_description = 'User Type'
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['enrollment_number', 'get_full_name', 'get_email', 'phone_number', 'created_at']
    search_fields = ['enrollment_number', 'user__first_name', 'user__last_name', 'user__email']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Student Details', {
            'fields': ('enrollment_number', 'date_of_birth', 'phone_number')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.full_name
    get_full_name.short_description = 'Full Name'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'get_full_name', 'specialization', 'get_email', 'created_at']
    search_fields = ['employee_id', 'user__first_name', 'user__last_name', 'specialization']
    list_filter = ['specialization', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Teacher Details', {
            'fields': ('employee_id', 'specialization', 'phone_number', 'bio')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.full_name
    get_full_name.short_description = 'Full Name'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)