from django.contrib import admin
from .models import Subject, Class


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'credits', 'created_at']
    search_fields = ['code', 'name']
    list_filter = ['credits', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Subject Information', {
            'fields': ('code', 'name', 'description', 'credits')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class ClassStudentInline(admin.TabularInline):
    model = Class.students.through
    extra = 1
    verbose_name = 'Enrolled Student'
    verbose_name_plural = 'Enrolled Students'


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['get_class_name', 'teacher', 'semester', 'schedule', 'room', 
                    'enrolled_count', 'max_students', 'is_active']
    list_filter = ['semester', 'is_active', 'subject', 'created_at']
    search_fields = ['subject__code', 'subject__name', 'teacher__user__last_name', 'room']
    readonly_fields = ['created_at', 'updated_at', 'enrolled_count', 'available_seats']
    filter_horizontal = ['students']
    
    fieldsets = (
        ('Class Information', {
            'fields': ('subject', 'teacher', 'semester')
        }),
        ('Schedule & Location', {
            'fields': ('schedule', 'room')
        }),
        ('Enrollment', {
            'fields': ('max_students', 'students')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Statistics', {
            'fields': ('enrolled_count', 'available_seats'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_class_name(self, obj):
        return str(obj)
    get_class_name.short_description = 'Class'
    
    def enrolled_count(self, obj):
        return obj.enrolled_count
    enrolled_count.short_description = 'Enrolled'