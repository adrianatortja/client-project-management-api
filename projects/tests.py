from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Project, Task

User = get_user_model()


class ProjectAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='otheruser@example.com',
            password='testpass123'
        )

        self.project = Project.objects.create(
            user=self.user,
            title='Client Portal Updated',
            description='Backend for managing client projects',
            status='active'
        )

        self.other_project = Project.objects.create(
            user=self.other_user,
            title='Other User Project',
            description='Should not appear',
            status='active'
        )

        Task.objects.create(
            project=self.project,
            title='First task',
            description='Completed task',
            completed=True
        )

        Task.objects.create(
            project=self.project,
            title='Second task',
            description='Pending task',
            completed=False
        )

        self.client.force_authenticate(user=self.user)

    def test_authenticated_user_can_list_own_projects(self):
        response = self.client.get('/api/projects/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Client Portal Updated')

    def test_project_response_includes_task_stats(self):
        response = self.client.get('/api/projects/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['total_tasks'], 2)
        self.assertEqual(response.data[0]['completed_tasks'], 1)
        self.assertEqual(response.data[0]['pending_tasks'], 1)

    def test_project_response_includes_nested_tasks(self):
        response = self.client.get('/api/projects/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tasks', response.data[0])
        self.assertEqual(len(response.data[0]['tasks']), 2)
        self.assertEqual(response.data[0]['tasks'][0]['project_title'], 'Client Portal Updated')

    def test_user_only_sees_own_projects(self):
        response = self.client.get('/api/projects/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [project['title'] for project in response.data]

        self.assertIn('Client Portal Updated', titles)
        self.assertNotIn('Other User Project', titles)
        