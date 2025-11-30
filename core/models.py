from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import Teacher, Student


class Subject(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    credits = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Class(models.Model):
    SEMESTER_CHOICES = [
        ('2024.1', '2024.1'),
        ('2024.2', '2024.2'),
        ('2025.1', '2025.1'),
        ('2025.2', '2025.2'),
    ]
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='classes')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='classes')
    students = models.ManyToManyField(Student, related_name='enrolled_classes', blank=True)
    
    schedule = models.CharField(max_length=100, help_text="e.g., MON 14:00-16:00")
    room = models.CharField(max_length=50, blank=True)
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES, default='2025.1')
    max_students = models.IntegerField(default=40, validators=[MinValueValidator(1)])
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-semester', 'subject__code']
        verbose_name_plural = 'Classes'
        unique_together = ['subject', 'teacher', 'schedule', 'semester']
    
    def __str__(self):
        return f"{self.subject.code} - {self.teacher.user.last_name} ({self.semester})"
    
    @property
    def enrolled_count(self):
        return self.students.count()
    
    @property
    def available_seats(self):
        return self.max_students - self.enrolled_count
    
    @property
    def is_full(self):
        return self.enrolled_count >= self.max_students
    
    def can_enroll(self, student):
        if self.is_full:
            return False, "Class is full"
        if student in self.students.all():
            return False, "Already enrolled"
        return True, "Can enroll"