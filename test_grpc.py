import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from backend_service.grpc_client import (
    enroll_student_grpc,
    unenroll_student_grpc,
    create_class_grpc,
    get_class_grpc,
    list_classes_grpc,
    get_teacher_classes_grpc,
    get_student_classes_grpc
)


def test_list_classes():
    """Test listing classes"""
    print("\n" + "="*60)
    print("TEST 1: List All Classes")
    print("="*60)
    
    try:
        classes = list_classes_grpc(semester='2025.1', active_only=True)
        print(f"✓ Found {len(classes)} classes")
        
        for c in classes[:3]:  # Show first 3
            print(f"\n  Class ID: {c.id}")
            print(f"  Subject: {c.subject_code} - {c.subject_name}")
            print(f"  Teacher: {c.teacher_name}")
            print(f"  Schedule: {c.schedule}")
            print(f"  Enrolled: {c.enrolled_count}/{c.max_students}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_get_class():
    """Test getting class details"""
    print("\n" + "="*60)
    print("TEST 2: Get Class Details")
    print("="*60)
    
    try:
        class_detail = get_class_grpc(1)
        print(f"✓ Class retrieved successfully")
        print(f"\n  Subject: {class_detail.subject.code} - {class_detail.subject.name}")
        print(f"  Teacher: {class_detail.teacher.full_name}")
        print(f"  Schedule: {class_detail.schedule}")
        print(f"  Room: {class_detail.room}")
        print(f"  Enrolled Students: {len(class_detail.students)}")
        
        for student in class_detail.students[:3]:  # Show first 3
            print(f"    - {student.full_name} ({student.enrollment_number})")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_enroll_student():
    """Test enrolling a student"""
    print("\n" + "="*60)
    print("TEST 3: Enroll Student")
    print("="*60)
    
    try:
        # Try to enroll student ID 5 in class ID 5
        result = enroll_student_grpc(class_id=5, student_id=5)
        
        if result['success']:
            print(f"✓ {result['message']}")
        else:
            print(f"⚠ {result['message']}")  # Might already be enrolled
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_get_teacher_classes():
    """Test getting teacher's classes"""
    print("\n" + "="*60)
    print("TEST 4: Get Teacher Classes")
    print("="*60)
    
    try:
        classes = get_teacher_classes_grpc(teacher_id=1, semester='2025.1')
        print(f"✓ Found {len(classes)} classes for teacher")
        
        for c in classes:
            print(f"\n  {c.subject_code} - {c.subject_name}")
            print(f"  Schedule: {c.schedule}")
            print(f"  Enrolled: {c.enrolled_count}/{c.max_students}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_get_student_classes():
    """Test getting student's classes"""
    print("\n" + "="*60)
    print("TEST 5: Get Student Classes")
    print("="*60)
    
    try:
        classes = get_student_classes_grpc(student_id=1, semester='2025.1')
        print(f"✓ Found {len(classes)} enrolled classes for student")
        
        for c in classes:
            print(f"\n  {c.subject_code} - {c.subject_name}")
            print(f"  Teacher: {c.teacher_name}")
            print(f"  Schedule: {c.schedule}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def run_all_tests():
    """Run all gRPC tests"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "gRPC TESTING SUITE" + " "*25 + "║")
    print("╚" + "="*58 + "╝")
    
    tests = [
        test_list_classes,
        test_get_class,
        test_enroll_student,
        test_get_teacher_classes,
        test_get_student_classes,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! gRPC is working correctly!")
    else:
        print(f"⚠ {total - passed} test(s) failed")
    print("="*60 + "\n")


if __name__ == '__main__':
    print("\n⚠ Make sure gRPC server is running before testing!")
    print("Start it with: python backend_service/grpc_server.py\n")
    
    input("Press Enter to start tests...")
    
    run_all_tests()