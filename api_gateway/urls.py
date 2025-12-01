from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'classes', views.ClassViewSet, basename='class')
router.register(r'subjects', views.SubjectViewSet, basename='subject')
router.register(r'students', views.StudentViewSet, basename='student')
router.register(r'teachers', views.TeacherViewSet, basename='teacher')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    # Additional custom endpoints
    path('my-classes/', views.MyClassesView.as_view(), name='my_classes'),
]