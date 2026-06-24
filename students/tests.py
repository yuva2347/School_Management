from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import RoleMaster
from students.forms import StudentForm, UpdateMarksForm
from students.models import Student
from teachers.models import Teacher


class TeacherDashboardAssignmentTests(TestCase):
    def setUp(self):
        self.teacher_user = get_user_model().objects.create_user(username='teacher1', password='secret123')
        RoleMaster.objects.create(username='teacher1', password='secret123', role='teacher')
        self.teacher = Teacher.objects.create(
            user=self.teacher_user,
            teacher_id='T001',
            subject='Mathematics',
            email='teacher@example.com',
        )

        self.assigned_user = get_user_model().objects.create_user(username='student1', password='secret123')
        self.assigned_student = Student.objects.create(
            user=self.assigned_user,
            student_id='S001',
            grade='A',
            marks=90,
            email='student1@example.com',
            assigned_teacher=self.teacher,
        )

        self.unassigned_user = get_user_model().objects.create_user(username='student2', password='secret123')
        self.unassigned_student = Student.objects.create(
            user=self.unassigned_user,
            student_id='S002',
            grade='B',
            marks=80,
            email='student2@example.com',
        )

    def test_teacher_dashboard_shows_only_assigned_students(self):
        self.client.force_login(self.teacher_user)
        response = self.client.get(reverse('teacher_dashboard'))

        self.assertEqual(response.status_code, 200)
        students = response.context['students']
        self.assertIn(self.assigned_student, students)
        self.assertNotIn(self.unassigned_student, students)

    def test_update_marks_form_allows_grade_and_marks_editing(self):
        form = UpdateMarksForm(instance=self.assigned_student)

        self.assertIn('grade', form.fields)
        self.assertIn('marks', form.fields)

    def test_student_form_lists_teachers_clearly(self):
        form = StudentForm()

        self.assertIn('assigned_teacher', form.fields)
        self.assertEqual(form.fields['assigned_teacher'].label, 'Assign Teacher')
