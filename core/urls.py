from django.urls import path
from . import views

app_name = 'classes'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Class views
    path('', views.class_list, name='list'),
    path('<int:pk>/', views.class_detail, name='detail'),
    path('create/', views.class_create, name='create'),
    path('<int:pk>/edit/', views.class_edit, name='edit'),
    path('<int:pk>/delete/', views.class_delete, name='delete'),
    
    # Enrollment
    path('<int:pk>/enroll/', views.enroll_class, name='enroll'),
    path('<int:pk>/unenroll/', views.unenroll_class, name='unenroll'),
    
    # My classes
    path('my-classes/', views.my_classes, name='my_classes'),
    path('my-teaching/', views.my_teaching, name='my_teaching'),
    
    # Subjects
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/create/', views.subject_create, name='subject_create'),
]