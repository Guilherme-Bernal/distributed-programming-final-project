from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from core.models import Class, Subject
from accounts.models import Student, Teacher
from backend_service.services import EnrollmentService, ClassService


# Serializers
from rest_framework import serializers

class SubjectSerializer(serializers.ModelSerializer):
    class_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Subject
        fields = ['id', 'code', 'name', 'description', 'credits', 'class_count']
    
    def get_class_count(self, obj):
        return obj.classes.count()


class TeacherSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Teacher
        fields = ['id', 'employee_id', 'full_name', 'specialization', 'email']


class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'enrollment_number', 'full_name', 'email']


class ClassListSerializer(serializers.ModelSerializer):
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.full_name', read_only=True)
    enrolled_count = serializers.IntegerField(read_only=True)
    available_seats = serializers.IntegerField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Class
        fields = [
            'id', 'subject_code', 'subject_name', 'teacher_name',
            'schedule', 'room', 'semester', 'max_students',
            'enrolled_count', 'available_seats', 'is_full', 'is_active'
        ]


class ClassDetailSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)
    students = StudentSerializer(many=True, read_only=True)
    enrolled_count = serializers.IntegerField(read_only=True)
    available_seats = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Class
        fields = [
            'id', 'subject', 'teacher', 'students', 'schedule', 'room',
            'semester', 'max_students', 'enrolled_count', 'available_seats',
            'is_active', 'created_at'
        ]


# ViewSets (keep the same as before)
class ClassViewSet(viewsets.ModelViewSet):
    """
    API endpoint for classes
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Class.objects.filter(is_active=True).select_related(
            'subject', 'teacher', 'teacher__user'
        ).prefetch_related('students')
        
        semester = self.request.query_params.get('semester')
        if semester:
            queryset = queryset.filter(semester=semester)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ClassDetailSerializer
        return ClassListSerializer
    
    def create(self, request):
        result = ClassService.create_class(request.data)
        
        if result['success']:
            class_obj = Class.objects.get(id=result['class_id'])
            serializer = ClassDetailSerializer(class_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'error': result['message']},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def enroll(self, request, pk=None):
        if not hasattr(request.user, 'student_profile'):
            return Response(
                {'error': 'Only students can enroll'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        student_id = request.user.student_profile.id
        result = EnrollmentService.enroll_student(pk, student_id)
        
        if result['success']:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unenroll(self, request, pk=None):
        if not hasattr(request.user, 'student_profile'):
            return Response(
                {'error': 'Only students can unenroll'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        student_id = request.user.student_profile.id
        result = EnrollmentService.unenroll_student(pk, student_id)
        
        if result['success']:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.all().order_by('code')
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.select_related('user').all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Teacher.objects.select_related('user').all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MyClassesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if hasattr(request.user, 'student_profile'):
            classes = request.user.student_profile.enrolled_classes.filter(is_active=True)
            serializer = ClassListSerializer(classes, many=True)
            return Response({
                'user_type': 'student',
                'classes': serializer.data
            })
        elif hasattr(request.user, 'teacher_profile'):
            classes = request.user.teacher_profile.classes.filter(is_active=True)
            serializer = ClassListSerializer(classes, many=True)
            return Response({
                'user_type': 'teacher',
                'classes': serializer.data
            })
        else:
            return Response(
                {'error': 'User has no student or teacher profile'},
                status=status.HTTP_400_BAD_REQUEST
            )