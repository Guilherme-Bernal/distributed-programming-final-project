from django.db import transaction
from django.core.exceptions import ValidationError
from accounts.models import Student, Teacher
from core.models import Subject, Class
import logging

logger = logging.getLogger('backend_service')


class EnrollmentService:
    """Handles student enrollment logic"""
    
    @staticmethod
    @transaction.atomic
    def enroll_student(class_id: int, student_id: int) -> dict:
        """
        Enroll a student in a class
        Returns: {'success': bool, 'message': str}
        """
        try:
            # Get class and student with row-level locking
            class_obj = Class.objects.select_for_update().get(id=class_id)
            student = Student.objects.get(id=student_id)
            
            # Business rule: Check if class is active
            if not class_obj.is_active:
                return {'success': False, 'message': 'Class is not active'}
            
            # Business rule: Check if class is full
            if class_obj.is_full:
                return {'success': False, 'message': 'Class is full'}
            
            # Business rule: Check if already enrolled
            if student in class_obj.students.all():
                return {'success': False, 'message': 'Student already enrolled'}
            
            # Business rule: Check schedule conflicts
            conflict = EnrollmentService._check_schedule_conflict(student, class_obj)
            if conflict:
                return {
                    'success': False,
                    'message': f'Schedule conflict with {conflict.subject.code}'
                }
            
            # Enroll student
            class_obj.students.add(student)
            
            logger.info(f"Student {student.enrollment_number} enrolled in {class_obj}")
            
            return {
                'success': True,
                'message': 'Enrolled successfully',
                'class_id': class_obj.id,
                'student_id': student.id
            }
            
        except Class.DoesNotExist:
            return {'success': False, 'message': 'Class not found'}
        except Student.DoesNotExist:
            return {'success': False, 'message': 'Student not found'}
        except Exception as e:
            logger.error(f"Error enrolling student: {str(e)}")
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    @staticmethod
    @transaction.atomic
    def unenroll_student(class_id: int, student_id: int) -> dict:
        """
        Unenroll a student from a class
        Returns: {'success': bool, 'message': str}
        """
        try:
            class_obj = Class.objects.select_for_update().get(id=class_id)
            student = Student.objects.get(id=student_id)
            
            if student not in class_obj.students.all():
                return {'success': False, 'message': 'Student not enrolled in this class'}
            
            class_obj.students.remove(student)
            
            logger.info(f"Student {student.enrollment_number} unenrolled from {class_obj}")
            
            return {
                'success': True,
                'message': 'Unenrolled successfully'
            }
            
        except Class.DoesNotExist:
            return {'success': False, 'message': 'Class not found'}
        except Student.DoesNotExist:
            return {'success': False, 'message': 'Student not found'}
        except Exception as e:
            logger.error(f"Error unenrolling student: {str(e)}")
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    @staticmethod
    def _check_schedule_conflict(student: Student, new_class: Class) -> Class:
        """
        Check if student has schedule conflict
        Returns: Conflicting class or None
        """
        enrolled_classes = student.enrolled_classes.filter(
            semester=new_class.semester,
            is_active=True
        )
        
        for enrolled_class in enrolled_classes:
            if EnrollmentService._schedules_overlap(
                enrolled_class.schedule,
                new_class.schedule
            ):
                return enrolled_class
        
        return None
    
    @staticmethod
    def _schedules_overlap(schedule1: str, schedule2: str) -> bool:
        """
        Simple schedule overlap check
        Format: "MON 14:00-16:00"
        TODO: Implement proper time parsing
        """
        # Extract day from schedule
        day1 = schedule1.split()[0] if schedule1 else ''
        day2 = schedule2.split()[0] if schedule2 else ''
        
        # Simple check: same day means potential conflict
        # In production, parse actual times
        return day1 == day2


class ClassService:
    """Handles class CRUD operations"""
    
    @staticmethod
    @transaction.atomic
    def create_class(data: dict) -> dict:
        """
        Create a new class
        Returns: {'success': bool, 'message': str, 'class_id': int}
        """
        try:
            # Validate required fields
            required_fields = ['subject_id', 'teacher_id', 'schedule', 'semester']
            for field in required_fields:
                if field not in data:
                    return {'success': False, 'message': f'Missing required field: {field}'}
            
            # Get related objects
            subject = Subject.objects.get(id=data['subject_id'])
            teacher = Teacher.objects.get(id=data['teacher_id'])
            
            # Business rule: Check for duplicate class
            existing = Class.objects.filter(
                subject=subject,
                teacher=teacher,
                schedule=data['schedule'],
                semester=data['semester']
            ).exists()
            
            if existing:
                return {'success': False, 'message': 'Class already exists with same details'}
            
            # Create class
            new_class = Class.objects.create(
                subject=subject,
                teacher=teacher,
                schedule=data['schedule'],
                semester=data['semester'],
                room=data.get('room', ''),
                max_students=data.get('max_students', 40),
                is_active=data.get('is_active', True)
            )
            
            logger.info(f"Class created: {new_class}")
            
            return {
                'success': True,
                'message': 'Class created successfully',
                'class_id': new_class.id
            }
            
        except Subject.DoesNotExist:
            return {'success': False, 'message': 'Subject not found'}
        except Teacher.DoesNotExist:
            return {'success': False, 'message': 'Teacher not found'}
        except Exception as e:
            logger.error(f"Error creating class: {str(e)}")
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    @staticmethod
    def get_teacher_classes(teacher_id: int, semester: str = None) -> list:
        """Get all classes for a teacher"""
        try:
            teacher = Teacher.objects.get(id=teacher_id)
            classes = teacher.classes.filter(is_active=True)
            
            if semester:
                classes = classes.filter(semester=semester)
            
            return classes
            
        except Teacher.DoesNotExist:
            return []
    
    @staticmethod
    def get_student_classes(student_id: int, semester: str = None) -> list:
        """Get all enrolled classes for a student"""
        try:
            student = Student.objects.get(id=student_id)
            classes = student.enrolled_classes.filter(is_active=True)
            
            if semester:
                classes = classes.filter(semester=semester)
            
            return classes
            
        except Student.DoesNotExist:
            return []


class SubjectService:
    """Handles subject CRUD operations"""
    
    @staticmethod
    def create_subject(data: dict) -> dict:
        """Create a new subject"""
        try:
            required_fields = ['code', 'name', 'credits']
            for field in required_fields:
                if field not in data:
                    return {'success': False, 'message': f'Missing required field: {field}'}
            
            # Check for duplicate code
            if Subject.objects.filter(code=data['code']).exists():
                return {'success': False, 'message': 'Subject code already exists'}
            
            subject = Subject.objects.create(
                code=data['code'],
                name=data['name'],
                credits=data['credits'],
                description=data.get('description', '')
            )
            
            logger.info(f"Subject created: {subject}")
            
            return {
                'success': True,
                'message': 'Subject created successfully',
                'subject_id': subject.id
            }
            
        except Exception as e:
            logger.error(f"Error creating subject: {str(e)}")
            return {'success': False, 'message': f'Error: {str(e)}'}