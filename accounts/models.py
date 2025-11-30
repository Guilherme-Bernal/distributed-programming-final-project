from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    enrollment_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.enrollment_number})"
    
    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    specialization = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']
    
    def __str__(self):
        return f"Prof. {self.user.get_full_name()} - {self.specialization}"
    
    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff and not instance.is_superuser:
            Teacher.objects.get_or_create(
                user=instance,
                defaults={'employee_id': f'T{instance.id:05d}', 'specialization': 'General'}
            )
        elif not instance.is_staff:
            Student.objects.get_or_create(
                user=instance,
                defaults={'enrollment_number': f'S{instance.id:05d}'}
            )