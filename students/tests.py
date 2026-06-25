from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import RoleMaster
from students.forms import StudentForm, UpdateMarksForm
from students.models import Student
from teachers.models import Teacher


class ForgotPasswordTests(TestCase):
    def test_forgot_password_resets_password_for_matching_email(self):
        user = get_user_model().objects.create_user(username='resetuser', email='reset@example.com', password='oldpass')
        RoleMaster.objects.create(username='resetuser', password='oldpass', role='student')

        response = self.client.post(reverse('forgot_password'), {
            'email': 'reset@example.com',
            'new_password': 'newpass123',
        })

        user.refresh_from_db()
        self.assertTrue(user.check_password('newpass123'))
        self.assertEqual(response.status_code, 200)

    def test_forgot_password_resets_password_for_teacher_profile_email(self):
        teacher_user = get_user_model().objects.create_user(username='teacherreset', password='oldpass')
        Teacher.objects.create(
            user=teacher_user,
            teacher_id='T999',
            subject='Science',
            email='teacherreset@example.com',
        )
        RoleMaster.objects.create(username='teacherreset', password='oldpass', role='teacher')

        response = self.client.post(reverse('forgot_password'), {
            'email': 'teacherreset@example.com',
            'new_password': 'newpass456',
        })

        teacher_user.refresh_from_db()
        self.assertTrue(teacher_user.check_password('newpass456'))
        self.assertEqual(response.status_code, 200)


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
