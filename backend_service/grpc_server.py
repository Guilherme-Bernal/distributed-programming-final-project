import grpc
from concurrent import futures
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

# Import generated gRPC code
from backend_service import classes_pb2, classes_pb2_grpc
from backend_service.services import EnrollmentService, ClassService
from core.models import Class, Subject
from accounts.models import Teacher, Student


class ClassServiceServicer(classes_pb2_grpc.ClassServiceServicer):
    """Implementation of ClassService gRPC service"""
    
    def EnrollStudent(self, request, context):
        """Enroll a student in a class"""
        print(f"[gRPC] EnrollStudent called: class_id={request.class_id}, student_id={request.student_id}")
        
        result = EnrollmentService.enroll_student(request.class_id, request.student_id)
        
        return classes_pb2.EnrollmentResponse(
            success=result['success'],
            message=result['message'],
            class_id=result.get('class_id', 0),
            student_id=result.get('student_id', 0)
        )
    
    def UnenrollStudent(self, request, context):
        """Unenroll a student from a class"""
        print(f"[gRPC] UnenrollStudent called: class_id={request.class_id}, student_id={request.student_id}")
        
        result = EnrollmentService.unenroll_student(request.class_id, request.student_id)
        
        return classes_pb2.EnrollmentResponse(
            success=result['success'],
            message=result['message'],
            class_id=0,
            student_id=0
        )
    
    def CreateClass(self, request, context):
        """Create a new class"""
        print(f"[gRPC] CreateClass called: subject_id={request.subject_id}, teacher_id={request.teacher_id}")
        
        data = {
            'subject_id': request.subject_id,
            'teacher_id': request.teacher_id,
            'schedule': request.schedule,
            'room': request.room,
            'semester': request.semester,
            'max_students': request.max_students,
            'is_active': request.is_active,
        }
        
        result = ClassService.create_class(data)
        
        return classes_pb2.ClassResponse(
            success=result['success'],
            message=result['message'],
            class_id=result.get('class_id', 0)
        )
    
    def GetClass(self, request, context):
        """Get detailed information about a class"""
        print(f"[gRPC] GetClass called: class_id={request.class_id}")
        
        try:
            class_obj = Class.objects.select_related('subject', 'teacher', 'teacher__user').prefetch_related('students', 'students__user').get(id=request.class_id)
            
            # Build response
            subject_info = classes_pb2.SubjectInfo(
                id=class_obj.subject.id,
                code=class_obj.subject.code,
                name=class_obj.subject.name,
                description=class_obj.subject.description,
                credits=class_obj.subject.credits
            )
            
            teacher_info = classes_pb2.TeacherInfo(
                id=class_obj.teacher.id,
                employee_id=class_obj.teacher.employee_id,
                full_name=class_obj.teacher.full_name,
                specialization=class_obj.teacher.specialization,
                email=class_obj.teacher.user.email
            )
            
            students_info = [
                classes_pb2.StudentInfo(
                    id=student.id,
                    enrollment_number=student.enrollment_number,
                    full_name=student.full_name,
                    email=student.user.email
                )
                for student in class_obj.students.all()
            ]
            
            return classes_pb2.ClassDetailResponse(
                id=class_obj.id,
                subject=subject_info,
                teacher=teacher_info,
                students=students_info,
                schedule=class_obj.schedule,
                room=class_obj.room or '',
                semester=class_obj.semester,
                max_students=class_obj.max_students,
                enrolled_count=class_obj.enrolled_count,
                available_seats=class_obj.available_seats,
                is_active=class_obj.is_active
            )
            
        except Class.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'Class with id {request.class_id} not found')
            return classes_pb2.ClassDetailResponse()
    
    def ListClasses(self, request, context):
        """List all classes with optional filtering"""
        print(f"[gRPC] ListClasses called: semester={request.semester}, active_only={request.active_only}")
        
        classes = Class.objects.select_related('subject', 'teacher', 'teacher__user').prefetch_related('students')
        
        if request.active_only:
            classes = classes.filter(is_active=True)
        
        if request.semester:
            classes = classes.filter(semester=request.semester)
        
        class_summaries = [
            classes_pb2.ClassSummary(
                id=c.id,
                subject_code=c.subject.code,
                subject_name=c.subject.name,
                teacher_name=c.teacher.full_name,
                schedule=c.schedule,
                room=c.room or '',
                semester=c.semester,
                max_students=c.max_students,
                enrolled_count=c.enrolled_count,
                available_seats=c.available_seats,
                is_full=c.is_full,
                is_active=c.is_active
            )
            for c in classes
        ]
        
        return classes_pb2.ListClassesResponse(classes=class_summaries)
    
    def GetTeacherClasses(self, request, context):
        """Get all classes for a specific teacher"""
        print(f"[gRPC] GetTeacherClasses called: teacher_id={request.teacher_id}")
        
        classes = ClassService.get_teacher_classes(request.teacher_id, request.semester or None)
        
        class_summaries = [
            classes_pb2.ClassSummary(
                id=c.id,
                subject_code=c.subject.code,
                subject_name=c.subject.name,
                teacher_name=c.teacher.full_name,
                schedule=c.schedule,
                room=c.room or '',
                semester=c.semester,
                max_students=c.max_students,
                enrolled_count=c.enrolled_count,
                available_seats=c.available_seats,
                is_full=c.is_full,
                is_active=c.is_active
            )
            for c in classes
        ]
        
        return classes_pb2.ListClassesResponse(classes=class_summaries)
    
    def GetStudentClasses(self, request, context):
        """Get all classes for a specific student"""
        print(f"[gRPC] GetStudentClasses called: student_id={request.student_id}")
        
        classes = ClassService.get_student_classes(request.student_id, request.semester or None)
        
        class_summaries = [
            classes_pb2.ClassSummary(
                id=c.id,
                subject_code=c.subject.code,
                subject_name=c.subject.name,
                teacher_name=c.teacher.full_name,
                schedule=c.schedule,
                room=c.room or '',
                semester=c.semester,
                max_students=c.max_students,
                enrolled_count=c.enrolled_count,
                available_seats=c.available_seats,
                is_full=c.is_full,
                is_active=c.is_active
            )
            for c in classes
        ]
        
        return classes_pb2.ListClassesResponse(classes=class_summaries)


def serve():
    """Start gRPC server"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    classes_pb2_grpc.add_ClassServiceServicer_to_server(
        ClassServiceServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    print('[gRPC Server] Starting on port 50051...')
    server.start()
    print('[gRPC Server] Ready to accept connections')
    server.wait_for_termination()


if __name__ == '__main__':
    serve()