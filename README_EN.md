# 🎓 Class Manager - Distributed Programming Final Project

A comprehensive class management system built with Django, featuring REST API and gRPC communication layers. This project demonstrates modern web architecture with microservices communication.

![Django](https://img.shields.io/badge/Django-5.0-green.svg)
![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![gRPC](https://img.shields.io/badge/gRPC-1.60.0-orange.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)



---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Technologies](#-technologies)
- [Quick Start](#-quick-start-docker)
- [Manual Installation](#-manual-installation)
- [User Credentials](#-default-user-credentials)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Screenshots](#-screenshots)
- [Development](#-development)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### For Students
- 📚 Browse available classes
- ✅ Enroll/unenroll in classes
- 📊 View enrolled classes and total credits
- 🔍 Search and filter classes by semester/subject
- ⚠️ Automatic schedule conflict detection
- 💺 Real-time seat availability

### For Teachers
- 👨‍🏫 Create and manage classes
- 👥 View enrolled students
- 📝 Edit class details (schedule, room, capacity)
- 📈 Teaching statistics dashboard
- 🗑️ Delete classes

### For Administrators
- 🎯 Complete system dashboard
- 📖 Manage subjects
- 👤 Manage users (students/teachers)
- 📊 View system-wide statistics
- ⚙️ Django admin panel access

### Technical Features
- 🔄 REST API for frontend communication (JSON)
- 🚀 gRPC for backend service communication
- 🎨 Modern UI with Tailwind CSS
- 🔐 Authentication and authorization
- 📱 Responsive design
- 🐳 Docker containerization
- ✅ Automated testing suite
- 📊 Business logic separation

---

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────────┐
│                    Frontend Layer                       │
│           (Django Templates + Tailwind CSS)             │
│                  http://localhost:8000                  │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP/HTML
┌────────────────────────▼────────────────────────────────┐
│                   Presentation Layer                    │
│            (Django Views + REST Framework)              │
│              GET/POST /api/classes/...                  │
└────────────────────────┬────────────────────────────────┘
                         │ gRPC (Port 50051)
┌────────────────────────▼────────────────────────────────┐
│                  Business Logic Layer                   │
│              (gRPC Server + Services)                   │
│         EnrollmentService, ClassService, etc.           │
└────────────────────────┬────────────────────────────────┘
                         │ ORM
┌────────────────────────▼────────────────────────────────┐
│                    Database Layer                       │
│                  SQLite / PostgreSQL                    │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technologies

### Backend
- **Django 5.0** - Web framework
- **Django REST Framework 3.14** - REST API
- **gRPC 1.60.0** - Inter-service communication
- **Protocol Buffers** - Data serialization
- **Python 3.13** - Programming language

### Frontend
- **Tailwind CSS 3.x** - Styling framework
- **Django Templates** - Server-side rendering
- **Vanilla JavaScript** - Interactions

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **SQLite** - Development database
- **PostgreSQL** - Production database (optional)

---

## 🚀 Quick Start (Docker)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed
- Git installed

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/distributed-programming-final-project.git
cd distributed-programming-final-project
```

### 2️⃣ Run with Docker Compose
```bash
# Build and start all services
docker-compose up --build
```

**Wait for the initialization to complete...**

### 3️⃣ Access the Application

- 🌐 **Web Interface:** http://localhost:8000
- 🔧 **Admin Panel:** http://localhost:8000/admin
- 📡 **REST API:** http://localhost:8000/api
- 📊 **Dashboard:** http://localhost:8000/classes/dashboard/
- 🔌 **gRPC Server:** localhost:50051

### 4️⃣ Stop the Application
```bash
# Stop containers
docker-compose down

# Stop and remove volumes (reset database)
docker-compose down -v
```

---

## 💻 Manual Installation

### Prerequisites
- Python 3.13+
- pip
- virtualenv (recommended)

### 1️⃣ Clone and Setup
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/distributed-programming-final-project.git
cd distributed-programming-final-project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Generate sample data
python manage.py create_sample_data

# Generate templates (if needed)
python manage.py generate_templates
```

### 3️⃣ Run Servers

**Terminal 1 - Django Server:**
```bash
python manage.py runserver
```

**Terminal 2 - gRPC Server:**
```bash
python backend_service/grpc_server.py
```

**Terminal 3 - Test gRPC (optional):**
```bash
python test_grpc.py
```

### 4️⃣ Access

Visit http://localhost:8000

---

## 🔐 Default User Credentials

### Administrator
```
Username: admin
Password: 12345678
Role: Full system access
```

### Teachers
```
Username: prof.silva
Password: teacher123
Role: Create/manage classes, view students

Username: prof.santos
Password: teacher123
Role: Mathematics teacher

Username: prof.oliveira
Password: teacher123
Role: Physics teacher

Username: prof.costa
Password: teacher123
Role: English teacher
```

### Students
```
Username: guilherme.aluno
Password: student123
Role: Enroll in classes, view schedule

Username: ana.student
Password: student123
Role: Student

Username: carlos.student
Password: student123
Role: Student

... (8 students total)
```

---

## 📡 API Documentation

### REST API Endpoints

#### Classes
```http
GET    /api/classes/              # List all classes
GET    /api/classes/{id}/         # Get class details
POST   /api/classes/              # Create class (teachers only)
POST   /api/classes/{id}/enroll/  # Enroll student
POST   /api/classes/{id}/unenroll/ # Unenroll student
```

#### Subjects
```http
GET    /api/subjects/             # List all subjects
GET    /api/subjects/{id}/        # Get subject details
```

#### Teachers
```http
GET    /api/teachers/             # List all teachers
GET    /api/teachers/{id}/        # Get teacher details
```

#### Students
```http
GET    /api/students/             # List all students (auth required)
GET    /api/students/{id}/        # Get student details
```

#### User-specific
```http
GET    /api/my-classes/           # Get current user's classes
```

### gRPC Endpoints
```protobuf
service ClassService {
    rpc EnrollStudent (EnrollmentRequest) returns (EnrollmentResponse);
    rpc UnenrollStudent (EnrollmentRequest) returns (EnrollmentResponse);
    rpc CreateClass (CreateClassRequest) returns (ClassResponse);
    rpc GetClass (GetClassRequest) returns (ClassDetailResponse);
    rpc ListClasses (ListClassesRequest) returns (ListClassesResponse);
    rpc GetTeacherClasses (GetTeacherClassesRequest) returns (ListClassesResponse);
    rpc GetStudentClasses (GetStudentClassesRequest) returns (ListClassesResponse);
}
```

### Example API Calls

**List Classes:**
```bash
curl http://localhost:8000/api/classes/
```

**Enroll in Class:**
```bash
curl -X POST http://localhost:8000/api/classes/1/enroll/ \
  -H "Authorization: Session YOUR_SESSION" \
  -H "Content-Type: application/json"
```

**Browse API:**
Visit http://localhost:8000/api/ in your browser for interactive API documentation.

---

## 📁 Project Structure
```
distributed-programming-final-project/
├── accounts/                    # User management app
│   ├── models.py               # Student, Teacher models
│   ├── views.py                # Authentication views
│   └── admin.py                # Admin configuration
├── core/                        # Core business logic app
│   ├── models.py               # Class, Subject models
│   ├── views.py                # Class management views
│   ├── services.py             # Business logic services
│   └── management/
│       └── commands/
│           ├── create_sample_data.py
│           └── generate_templates.py
├── api_gateway/                 # REST API app
│   ├── views.py                # API ViewSets
│   └── serializers.py          # DRF Serializers
├── backend_service/             # gRPC service app
│   ├── grpc_server.py          # gRPC server
│   ├── grpc_client.py          # gRPC client helper
│   ├── services.py             # Business logic
│   ├── classes_pb2.py          # Generated protobuf
│   └── classes_pb2_grpc.py     # Generated gRPC stubs
├── protos/
│   └── classes.proto           # Protocol Buffer definitions
├── templates/                   # HTML templates
│   ├── base/
│   │   └── base.html           # Base template
│   ├── accounts/               # Auth templates
│   └── classes/                # Class templates
├── static/                      # Static files
│   ├── css/
│   └── js/
├── config/                      # Django settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── Dockerfile                   # Django container
├── Dockerfile.grpc              # gRPC container
├── docker-compose.yml           # Multi-container setup
├── requirements.txt             # Python dependencies
├── manage.py                    # Django management
├── test_grpc.py                # gRPC test suite
└── README.md                    # This file
```

---

## 📸 Screenshots

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Class List
![Class List](docs/screenshots/class-list.png)

### Class Details
![Class Details](docs/screenshots/class-detail.png)

### Admin Panel
![Admin Panel](docs/screenshots/admin-panel.png)

---

## 🔧 Development

### Docker Commands
```bash
# View logs
docker-compose logs -f
docker-compose logs -f web    # Django only
docker-compose logs -f grpc   # gRPC only

# Run Django commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell

# Access container shell
docker-compose exec web bash
docker-compose exec grpc bash

# Rebuild containers
docker-compose up --build

# Clean everything
docker-compose down -v
```

### Management Commands
```bash
# Create sample data
python manage.py create_sample_data

# Generate missing templates
python manage.py generate_templates

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

### Regenerate gRPC Code
```bash
# Generate Python code from proto file
python -m grpc_tools.protoc \
  -I=protos \
  --python_out=backend_service \
  --grpc_python_out=backend_service \
  protos/classes.proto

# Fix imports
python fix_grpc_imports.py
```

---

## 🧪 Testing

### Run All Tests
```bash
# Django tests
python manage.py test

# gRPC tests
python test_grpc.py
```

### Test Coverage
```bash
# Install coverage
pip install coverage

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Test gRPC Endpoints
```bash
# Make sure gRPC server is running
python backend_service/grpc_server.py

# Run gRPC tests
python test_grpc.py
```

**Expected output:**
```
╔==========================================================╗
║               gRPC TESTING SUITE                         ║
╚==========================================================╝

TEST 1: List All Classes
✓ Found 9 classes

TEST 2: Get Class Details
✓ Class retrieved successfully

TEST 3: Enroll Student
✓ Enrolled successfully

TEST 4: Get Teacher Classes
✓ Found 5 classes for teacher

TEST 5: Get Student Classes
✓ Found 4 enrolled classes for student

============================================================
SUMMARY
============================================================
Tests Passed: 5/5
✓ All tests passed! gRPC is working correctly!
============================================================
```

---

## 🎯 Assignment Requirements

This project fulfills all requirements for the Distributed Programming Final Project:

✅ **Framework:** Django web framework  
✅ **REST API:** JSON API for frontend communication  
✅ **gRPC API:** Backend service communication  
✅ **Business Logic:** Separated in backend service layer  
✅ **Frontend API:** Prepares data for presentation  
✅ **CRUD Operations:** Complete for all entities  
✅ **Theme:** Class management system  
✅ **Entities:** Students, Teachers, Subjects, Classes  
✅ **Features:**
  - Student enrollment/unenrollment
  - Teacher class creation and management
  - Class browsing and filtering
  - Schedule conflict detection
  - Capacity management

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [gRPC Python Documentation](https://grpc.io/docs/languages/python/)
- [Protocol Buffers](https://developers.google.com/protocol-buffers)
- [Docker Documentation](https://docs.docker.com/)
- [Tailwind CSS](https://tailwindcss.com/)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the GNU License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Guilherme Ferreira**  
Computer Engineering Student - 10th Semester  
Facens University - São Paulo, Brazil  

- GitHub: [@Guilherme-Bernal](https://github.com/Guilherme-Bernal)
- LinkedIn: [LinkedIn](https://www.linkedin.com/in/guilherme-savassa-bernal/)


---

## 🙏 Acknowledgments

- Facens University - Distributed Programming Course
- MARCOS FABIO JARDINI 
- Django and gRPC communities
- All contributors and testers

---

## 📊 Project Statistics

- **Lines of Code:** ~5,000+
- **Models:** 4 (Student, Teacher, Subject, Class)
- **API Endpoints:** 15+
- **gRPC Methods:** 7
- **Templates:** 15+
- **Management Commands:** 2
- **Test Coverage:** 85%+


---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/YOUR_USERNAME/distributed-programming-final-project/issues) page
2. Create a new issue with detailed description
3. Contact the author via email

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star! ⭐**

Made with ❤️ for Distributed Programming Final Project

</div>
