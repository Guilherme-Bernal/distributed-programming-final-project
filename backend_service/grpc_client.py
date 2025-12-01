import grpc
from backend_service import classes_pb2, classes_pb2_grpc
from django.conf import settings


class GRPCClient:
    """Helper class for gRPC communication"""
    
    def __init__(self):
        self.host = getattr(settings, 'GRPC_SERVER_HOST', 'localhost')
        self.port = getattr(settings, 'GRPC_SERVER_PORT', 50051)
        self.channel = None
        self.stub = None
    
    def connect(self):
        """Establish connection to gRPC server"""
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
        self.stub = classes_pb2_grpc.ClassServiceStub(self.channel)
        return self.stub
    
    def close(self):
        """Close gRPC connection"""
        if self.channel:
            self.channel.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self.connect()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# Convenience functions
def enroll_student_grpc(class_id, student_id):
    """Enroll student via gRPC"""
    with GRPCClient() as stub:
        request = classes_pb2.EnrollmentRequest(
            class_id=class_id,
            student_id=student_id
        )
        response = stub.EnrollStudent(request)
        return {
            'success': response.success,
            'message': response.message,
            'class_id': response.class_id,
            'student_id': response.student_id
        }


def unenroll_student_grpc(class_id, student_id):
    """Unenroll student via gRPC"""
    with GRPCClient() as stub:
        request = classes_pb2.EnrollmentRequest(
            class_id=class_id,
            student_id=student_id
        )
        response = stub.UnenrollStudent(request)
        return {
            'success': response.success,
            'message': response.message
        }


def create_class_grpc(subject_id, teacher_id, schedule, room, semester, max_students, is_active=True):
    """Create class via gRPC"""
    with GRPCClient() as stub:
        request = classes_pb2.CreateClassRequest(
            subject_id=subject_id,
            teacher_id=teacher_id,
            schedule=schedule,
            room=room,
            semester=semester,
            max_students=max_students,
            is_active=is_active
        )
        response = stub.CreateClass(request)
        return {
            'success': response.success,
            'message': response.message,
            'class_id': response.class_id
        }


def get_class_grpc(class_id):
    """Get class details via gRPC"""
    with GRPCClient() as stub:
        request = classes_pb2.GetClassRequest(class_id=class_id)
        response = stub.GetClass(request)
        return response


def list_classes_grpc(semester='', active_only=True):
    """List classes via gRPC"""
    with GRPCClient() as stub:
        request = classes_pb2.ListClassesRequest(
            semester=semester,
            active_only=active_only
        )
        response = stub.ListClasses(request)
        return response.classes


def get_teacher_classes_grpc(teacher_id, semester=''):
    """Get teacher's classes via gRPC"""
    with GRPCClient() as stub:
        request = classes_pb2.GetTeacherClassesRequest(
            teacher_id=teacher_id,
            semester=semester
        )
        response = stub.GetTeacherClasses(request)
        return response.classes


def get_student_classes_grpc(student_id, semester=''):
    """Get student's classes via gRPC"""
    with GRPCClient() as stub:
        request = classes_pb2.GetStudentClassesRequest(
            student_id=student_id,
            semester=semester
        )
        response = stub.GetStudentClasses(request)
        return response.classes