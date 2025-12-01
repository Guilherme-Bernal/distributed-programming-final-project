from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Student, Teacher
from core.models import Subject, Class
from django.db import transaction


class Command(BaseCommand):
    help = 'Creates sample data for testing the application'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        
        with transaction.atomic():
            # Clear existing data (except superuser)
            self.stdout.write('Clearing existing data...')
            Class.objects.all().delete()
            Subject.objects.all().delete()
            Student.objects.all().delete()
            Teacher.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            
            # Create Subjects
            self.stdout.write('Creating subjects...')
            subjects_data = [
                {'code': 'CS101', 'name': 'Introduction to Computer Science', 'credits': 4, 
                 'description': 'Fundamental concepts of programming and computer science.'},
                {'code': 'CS201', 'name': 'Data Structures', 'credits': 4,
                 'description': 'Advanced data structures and algorithms.'},
                {'code': 'CS301', 'name': 'Database Systems', 'credits': 3,
                 'description': 'Relational databases, SQL, and database design.'},
                {'code': 'MATH201', 'name': 'Calculus I', 'credits': 4,
                 'description': 'Limits, derivatives, and integrals.'},
                {'code': 'MATH202', 'name': 'Linear Algebra', 'credits': 3,
                 'description': 'Vectors, matrices, and linear transformations.'},
                {'code': 'PHY101', 'name': 'Physics I', 'credits': 4,
                 'description': 'Mechanics, thermodynamics, and waves.'},
                {'code': 'ENG101', 'name': 'English Composition', 'credits': 3,
                 'description': 'Academic writing and critical thinking.'},
                {'code': 'CS401', 'name': 'Distributed Systems', 'credits': 4,
                 'description': 'Design and implementation of distributed systems.'},
            ]
            
            subjects = {}
            for data in subjects_data:
                subject = Subject.objects.create(**data)
                subjects[data['code']] = subject
                self.stdout.write(f'  ✓ Created subject: {subject.code}')
            
            # Create Teachers
            self.stdout.write('\nCreating teachers...')
            teachers_data = [
                {'username': 'prof.silva', 'first_name': 'João', 'last_name': 'Silva',
                 'email': 'joao.silva@university.edu', 'specialization': 'Computer Science',
                 'phone': '(15) 99999-1111'},
                {'username': 'prof.santos', 'first_name': 'Maria', 'last_name': 'Santos',
                 'email': 'maria.santos@university.edu', 'specialization': 'Mathematics',
                 'phone': '(15) 99999-1112'},
                {'username': 'prof.oliveira', 'first_name': 'Pedro', 'last_name': 'Oliveira',
                 'email': 'pedro.oliveira@university.edu', 'specialization': 'Physics',
                 'phone': '(15) 99999-1113'},
                {'username': 'prof.costa', 'first_name': 'Ana', 'last_name': 'Costa',
                 'email': 'ana.costa@university.edu', 'specialization': 'English Literature',
                 'phone': '(15) 99999-1114'},
            ]
            
            teachers = {}
            for data in teachers_data:
                phone = data.pop('phone')
                specialization = data.pop('specialization')
                
                user = User.objects.create_user(
                    password='teacher123',
                    is_staff=True,
                    **data
                )
                
                # Update teacher profile (created by signal)
                user.teacher_profile.specialization = specialization
                user.teacher_profile.phone_number = phone
                user.teacher_profile.save()
                
                teachers[data['username']] = user.teacher_profile
                self.stdout.write(f'  ✓ Created teacher: {user.get_full_name()}')
            
            # Create Students
            self.stdout.write('\nCreating students...')
            students_data = [
                {'username': 'guilherme.aluno', 'first_name': 'Guilherme', 'last_name': 'Ferreira',
                 'email': 'guilherme@student.edu', 'phone': '(15) 99999-2001'},
                {'username': 'ana.student', 'first_name': 'Ana', 'last_name': 'Costa',
                 'email': 'ana@student.edu', 'phone': '(15) 99999-2002'},
                {'username': 'carlos.student', 'first_name': 'Carlos', 'last_name': 'Ferreira',
                 'email': 'carlos@student.edu', 'phone': '(15) 99999-2003'},
                {'username': 'beatriz.student', 'first_name': 'Beatriz', 'last_name': 'Lima',
                 'email': 'beatriz@student.edu', 'phone': '(15) 99999-2004'},
                {'username': 'rafael.student', 'first_name': 'Rafael', 'last_name': 'Souza',
                 'email': 'rafael@student.edu', 'phone': '(15) 99999-2005'},
                {'username': 'julia.student', 'first_name': 'Julia', 'last_name': 'Oliveira',
                 'email': 'julia@student.edu', 'phone': '(15) 99999-2006'},
                {'username': 'lucas.student', 'first_name': 'Lucas', 'last_name': 'Pereira',
                 'email': 'lucas@student.edu', 'phone': '(15) 99999-2007'},
                {'username': 'mariana.student', 'first_name': 'Mariana', 'last_name': 'Santos',
                 'email': 'mariana@student.edu', 'phone': '(15) 99999-2008'},
            ]
            
            students = []
            for data in students_data:
                phone = data.pop('phone')
                
                user = User.objects.create_user(
                    password='student123',
                    is_staff=False,
                    **data
                )
                
                # Update student profile (created by signal)
                user.student_profile.phone_number = phone
                user.student_profile.save()
                
                students.append(user.student_profile)
                self.stdout.write(f'  ✓ Created student: {user.get_full_name()}')
            
            # Create Classes
            self.stdout.write('\nCreating classes...')
            classes_data = [
                {'subject': 'CS101', 'teacher': 'prof.silva', 'schedule': 'MON 14:00-16:00',
                 'room': 'Lab 101', 'semester': '2025.1', 'max_students': 40},
                {'subject': 'CS101', 'teacher': 'prof.silva', 'schedule': 'WED 10:00-12:00',
                 'room': 'Lab 102', 'semester': '2025.1', 'max_students': 35},
                {'subject': 'CS201', 'teacher': 'prof.silva', 'schedule': 'TUE 14:00-16:00',
                 'room': 'Lab 201', 'semester': '2025.1', 'max_students': 30},
                {'subject': 'CS301', 'teacher': 'prof.silva', 'schedule': 'THU 16:00-18:00',
                 'room': 'Lab 301', 'semester': '2025.1', 'max_students': 25},
                {'subject': 'CS401', 'teacher': 'prof.silva', 'schedule': 'FRI 14:00-17:00',
                 'room': 'Lab 401', 'semester': '2025.1', 'max_students': 20},
                {'subject': 'MATH201', 'teacher': 'prof.santos', 'schedule': 'MON 10:00-12:00',
                 'room': 'Room 202', 'semester': '2025.1', 'max_students': 45},
                {'subject': 'MATH202', 'teacher': 'prof.santos', 'schedule': 'WED 14:00-16:00',
                 'room': 'Room 203', 'semester': '2025.1', 'max_students': 40},
                {'subject': 'PHY101', 'teacher': 'prof.oliveira', 'schedule': 'TUE 10:00-12:00',
                 'room': 'Lab 303', 'semester': '2025.1', 'max_students': 35},
                {'subject': 'ENG101', 'teacher': 'prof.costa', 'schedule': 'THU 10:00-12:00',
                 'room': 'Room 104', 'semester': '2025.1', 'max_students': 30},
            ]
            
            created_classes = []
            for data in classes_data:
                class_obj = Class.objects.create(
                    subject=subjects[data['subject']],
                    teacher=teachers[data['teacher']],
                    schedule=data['schedule'],
                    room=data['room'],
                    semester=data['semester'],
                    max_students=data['max_students'],
                    is_active=True
                )
                created_classes.append(class_obj)
                self.stdout.write(f'  ✓ Created class: {class_obj}')
            
            # Enroll students in classes
            self.stdout.write('\nEnrolling students in classes...')
            
            # Guilherme enrolled in CS courses
            created_classes[0].students.add(students[0])  # CS101 MON
            created_classes[2].students.add(students[0])  # CS201
            created_classes[3].students.add(students[0])  # CS301
            created_classes[4].students.add(students[0])  # CS401
            self.stdout.write(f'  ✓ Enrolled {students[0].full_name} in 4 classes')
            
            # Ana enrolled in varied courses
            created_classes[0].students.add(students[1])  # CS101
            created_classes[5].students.add(students[1])  # MATH201
            created_classes[7].students.add(students[1])  # PHY101
            self.stdout.write(f'  ✓ Enrolled {students[1].full_name} in 3 classes')
            
            # Carlos enrolled in CS and Math
            created_classes[1].students.add(students[2])  # CS101 WED
            created_classes[5].students.add(students[2])  # MATH201
            created_classes[6].students.add(students[2])  # MATH202
            self.stdout.write(f'  ✓ Enrolled {students[2].full_name} in 3 classes')
            
            # Beatriz in mixed courses
            created_classes[0].students.add(students[3])  # CS101
            created_classes[8].students.add(students[3])  # ENG101
            self.stdout.write(f'  ✓ Enrolled {students[3].full_name} in 2 classes')
            
            # Other students in various classes
            for i in range(4, len(students)):
                # Enroll in 2-3 random classes
                import random
                num_classes = random.randint(2, 3)
                selected_classes = random.sample(created_classes, num_classes)
                
                for class_obj in selected_classes:
                    class_obj.students.add(students[i])
                
                self.stdout.write(f'  ✓ Enrolled {students[i].full_name} in {num_classes} classes')
            
            # Summary
            self.stdout.write('\n' + '='*60)
            self.stdout.write(self.style.SUCCESS('✓ Sample data created successfully!'))
            self.stdout.write('='*60)
            self.stdout.write(f'\n📊 Summary:')
            self.stdout.write(f'  • Subjects: {Subject.objects.count()}')
            self.stdout.write(f'  • Teachers: {Teacher.objects.count()}')
            self.stdout.write(f'  • Students: {Student.objects.count()}')
            self.stdout.write(f'  • Classes: {Class.objects.count()}')
            self.stdout.write(f'\n🔐 Login Credentials:')
            self.stdout.write(f'  Teachers: username=prof.silva, password=teacher123')
            self.stdout.write(f'  Students: username=guilherme.aluno, password=student123')
            self.stdout.write('='*60 + '\n')