"""
Management command to auto-generate missing templates
"""

from django.core.management.base import BaseCommand
from pathlib import Path
import os


class Command(BaseCommand):
    help = 'Auto-generate missing templates for the application'

    TEMPLATE_DIR = Path('templates/classes')
    
    TEMPLATES = {
        'detail.html': '''{% extends 'base/base.html' %}

{% block title %}Class Details - Class Manager{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto">
    <!-- Back Button -->
    <div class="mb-6">
        <a href="{% url 'classes:list' %}" class="text-blue-600 hover:text-blue-800 flex items-center">
            ← Back to All Classes
        </a>
    </div>

    <!-- Class Details Card -->
    <div class="bg-white rounded-lg shadow-lg p-8">
        <div class="flex justify-between items-start mb-6">
            <div>
                <span class="text-sm font-semibold text-blue-600 bg-blue-100 px-3 py-1 rounded-full">
                    {{ class.subject.code }}
                </span>
                <h2 class="text-3xl font-bold text-gray-800 mt-3">{{ class.subject.name }}</h2>
            </div>
            <span class="text-sm text-gray-500">{{ class.semester }}</span>
        </div>

        <!-- Class Information -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div>
                <h3 class="text-sm font-semibold text-gray-600 mb-3">Class Information</h3>
                <div class="space-y-3">
                    <div class="flex items-center">
                        <span class="text-gray-600 w-24">👨‍🏫 Teacher:</span>
                        <span class="font-semibold">{{ class.teacher.full_name }}</span>
                    </div>
                    <div class="flex items-center">
                        <span class="text-gray-600 w-24">🕐 Schedule:</span>
                        <span class="font-semibold">{{ class.schedule }}</span>
                    </div>
                    <div class="flex items-center">
                        <span class="text-gray-600 w-24">🚪 Room:</span>
                        <span class="font-semibold">{{ class.room|default:"TBA" }}</span>
                    </div>
                    <div class="flex items-center">
                        <span class="text-gray-600 w-24">📅 Semester:</span>
                        <span class="font-semibold">{{ class.semester }}</span>
                    </div>
                </div>
            </div>

            <div>
                <h3 class="text-sm font-semibold text-gray-600 mb-3">Enrollment Status</h3>
                <div class="space-y-3">
                    <div class="flex items-center">
                        <span class="text-gray-600 w-32">👥 Enrolled:</span>
                        <span class="font-semibold">{{ class.enrolled_count }}</span>
                    </div>
                    <div class="flex items-center">
                        <span class="text-gray-600 w-32">📊 Capacity:</span>
                        <span class="font-semibold">{{ class.max_students }}</span>
                    </div>
                    <div class="flex items-center">
                        <span class="text-gray-600 w-32">💺 Available:</span>
                        <span class="font-semibold {% if class.available_seats > 0 %}text-green-600{% else %}text-red-600{% endif %}">
                            {{ class.available_seats }}
                        </span>
                    </div>
                    <div class="flex items-center">
                        <span class="text-gray-600 w-32">📖 Credits:</span>
                        <span class="font-semibold">{{ class.subject.credits }}</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Subject Description -->
        {% if class.subject.description %}
        <div class="mb-8">
            <h3 class="text-sm font-semibold text-gray-600 mb-2">About This Subject</h3>
            <p class="text-gray-700">{{ class.subject.description }}</p>
        </div>
        {% endif %}

        <!-- Enrollment Actions (for students) -->
        {% if user.is_authenticated and user.student_profile %}
        <div class="border-t pt-6">
            {% if is_enrolled %}
                <div class="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
                    <p class="text-green-800 font-semibold">✓ You are enrolled in this class</p>
                </div>
                <form method="post" action="{% url 'classes:unenroll' class.pk %}">
                    {% csrf_token %}
                    <button type="submit" class="bg-red-500 hover:bg-red-600 text-white font-semibold py-3 px-8 rounded-lg transition-colors">
                        Unenroll from Class
                    </button>
                </form>
            {% else %}
                {% if class.is_full %}
                    <div class="bg-red-50 border border-red-200 rounded-lg p-4">
                        <p class="text-red-800 font-semibold">✗ This class is full</p>
                    </div>
                {% else %}
                    <form method="post" action="{% url 'classes:enroll' class.pk %}">
                        {% csrf_token %}
                        <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors">
                            Enroll in This Class
                        </button>
                    </form>
                {% endif %}
            {% endif %}
        </div>
        {% endif %}

        <!-- Edit Actions (for teachers/admin) -->
        {% if user.is_authenticated %}
            {% if user.teacher_profile and class.teacher == user.teacher_profile or user.is_staff %}
            <div class="border-t pt-6 mt-6">
                <div class="flex gap-4">
                    <a href="{% url 'classes:edit' class.pk %}" class="bg-yellow-500 hover:bg-yellow-600 text-white font-semibold py-3 px-8 rounded-lg transition-colors">
                        Edit Class
                    </a>
                    <form method="post" action="{% url 'classes:delete' class.pk %}" onsubmit="return confirm('Are you sure you want to delete this class?');">
                        {% csrf_token %}
                        <button type="submit" class="bg-red-500 hover:bg-red-600 text-white font-semibold py-3 px-8 rounded-lg transition-colors">
                            Delete Class
                        </button>
                    </form>
                </div>
            </div>
            {% endif %}
        {% endif %}

        <!-- Enrolled Students (for teachers) -->
        {% if user.is_authenticated and user.teacher_profile and class.teacher == user.teacher_profile or user.is_staff %}
        <div class="border-t pt-6 mt-6">
            <h3 class="text-lg font-bold mb-4">Enrolled Students ({{ class.enrolled_count }})</h3>
            {% if class.students.all %}
            <div class="bg-gray-50 rounded-lg p-4">
                <div class="space-y-2">
                    {% for student in class.students.all %}
                    <div class="flex items-center justify-between p-3 bg-white rounded border border-gray-200">
                        <div>
                            <p class="font-semibold">{{ student.full_name }}</p>
                            <p class="text-sm text-gray-600">{{ student.enrollment_number }}</p>
                        </div>
                        <p class="text-sm text-gray-600">{{ student.user.email }}</p>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% else %}
            <p class="text-gray-500 text-center py-4">No students enrolled yet</p>
            {% endif %}
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
''',

        'create.html': '''{% extends 'base/base.html' %}

{% block title %}Create Class - Class Manager{% endblock %}

{% block content %}
<div class="max-w-2xl mx-auto">
    <div class="mb-6">
        <a href="{% url 'classes:list' %}" class="text-blue-600 hover:text-blue-800">
            ← Back to Classes
        </a>
    </div>

    <div class="bg-white rounded-lg shadow-lg p-8">
        <h2 class="text-3xl font-bold text-gray-800 mb-6">Create New Class</h2>

        <form method="post" class="space-y-6">
            {% csrf_token %}

            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Subject *</label>
                <select name="subject" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                    <option value="">Select a subject</option>
                    {% for subject in subjects %}
                    <option value="{{ subject.id }}">{{ subject.code }} - {{ subject.name }}</option>
                    {% endfor %}
                </select>
            </div>

            {% if user.is_staff %}
            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Teacher *</label>
                <select name="teacher" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                    <option value="">Select a teacher</option>
                    {% for teacher in teachers %}
                    <option value="{{ teacher.id }}">{{ teacher.full_name }}</option>
                    {% endfor %}
                </select>
            </div>
            {% endif %}

            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Schedule *</label>
                <input type="text" name="schedule" required placeholder="e.g., MON 14:00-16:00" 
                       class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                <p class="text-xs text-gray-500 mt-1">Format: DAY HH:MM-HH:MM</p>
            </div>

            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Room</label>
                <input type="text" name="room" placeholder="e.g., Lab 101" 
                       class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
            </div>

            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Semester *</label>
                <select name="semester" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                    <option value="">Select semester</option>
                    <option value="2024.1">2024.1</option>
                    <option value="2024.2">2024.2</option>
                    <option value="2025.1">2025.1</option>
                    <option value="2025.2">2025.2</option>
                </select>
            </div>

            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Maximum Students *</label>
                <input type="number" name="max_students" value="40" min="1" max="100" required
                       class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
            </div>

            <div class="flex items-center">
                <input type="checkbox" name="is_active" id="is_active" checked class="w-4 h-4 text-blue-600">
                <label for="is_active" class="ml-2 text-sm text-gray-700">Active (students can enroll)</label>
            </div>

            <div class="flex gap-4">
                <button type="submit" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg transition-colors">
                    Create Class
                </button>
                <a href="{% url 'classes:list' %}" class="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 font-semibold py-3 rounded-lg text-center transition-colors">
                    Cancel
                </a>
            </div>
        </form>
    </div>
</div>
{% endblock %}
''',

        'edit.html': '''{% extends 'base/base.html' %}

{% block title %}Edit Class - Class Manager{% endblock %}

{% block content %}
<div class="max-w-2xl mx-auto">
    <div class="mb-6">
        <a href="{% url 'classes:detail' class.pk %}" class="text-blue-600 hover:text-blue-800">
            ← Back to Class Details
        </a>
    </div>

    <div class="bg-white rounded-lg shadow-lg p-8">
        <h2 class="text-3xl font-bold text-gray-800 mb-6">Edit Class</h2>

        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <p class="text-sm text-blue-800">
                <strong>{{ class.subject.code }}</strong> - {{ class.subject.name }}<br>
                Teacher: <strong>{{ class.teacher.full_name }}</strong>
            </p>
        </div>

        <form method="post" class="space-y-6">
            {% csrf_token %}

            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Schedule *</label>
                <input type="text" name="schedule" value="{{ class.schedule }}" required
                       class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
            </div>

            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Room</label>
                <input type="text" name="room" value="{{ class.room }}"
                       class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
            </div>

            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Semester *</label>
                <select name="semester" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                    <option value="2024.1" {% if class.semester == "2024.1" %}selected{% endif %}>2024.1</option>
                    <option value="2024.2" {% if class.semester == "2024.2" %}selected{% endif %}>2024.2</option>
                    <option value="2025.1" {% if class.semester == "2025.1" %}selected{% endif %}>2025.1</option>
                    <option value="2025.2" {% if class.semester == "2025.2" %}selected{% endif %}>2025.2</option>
                </select>
            </div>

            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Maximum Students *</label>
                <input type="number" name="max_students" value="{{ class.max_students }}" min="1" max="100" required
                       class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
            </div>

            <div class="flex items-center">
                <input type="checkbox" name="is_active" id="is_active" {% if class.is_active %}checked{% endif %} class="w-4 h-4 text-blue-600">
                <label for="is_active" class="ml-2 text-sm text-gray-700">Active (students can enroll)</label>
            </div>

            <div class="flex gap-4">
                <button type="submit" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg transition-colors">
                    Save Changes
                </button>
                <a href="{% url 'classes:detail' class.pk %}" class="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 font-semibold py-3 rounded-lg text-center transition-colors">
                    Cancel
                </a>
            </div>
        </form>
    </div>
</div>
{% endblock %}
''',
    }

    def handle(self, *args, **options):
        # Create templates directory if it doesn't exist
        self.TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
        
        created_count = 0
        skipped_count = 0
        
        for filename, content in self.TEMPLATES.items():
            filepath = self.TEMPLATE_DIR / filename
            
            if filepath.exists():
                self.stdout.write(self.style.WARNING(f'Skipped: {filename} (already exists)'))
                skipped_count += 1
            else:
                filepath.write_text(content, encoding='utf-8')
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {filename}'))
                created_count += 1
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'Templates generated: {created_count}'))
        self.stdout.write(self.style.WARNING(f'Templates skipped: {skipped_count}'))
        self.stdout.write('='*60)