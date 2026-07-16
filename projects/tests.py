from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from factories import (
    MembershipFactory,
    OrganizationFactory,
    ProjectFactory,
    SubscriptionFactory,
    TaskFactory,
    UserFactory,
)
from orgs.models import Membership


class ProjectAPITests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()

        self.org = OrganizationFactory()
        MembershipFactory(organization=self.org, user=self.user, role=Membership.ROLE_OWNER)
        SubscriptionFactory(organization=self.org)

        self.other_org = OrganizationFactory()
        MembershipFactory(organization=self.other_org, user=self.other_user, role=Membership.ROLE_OWNER)
        SubscriptionFactory(organization=self.other_org)

        self.project = ProjectFactory(
            organization=self.org,
            created_by=self.user,
            title='Client Portal Updated',
            description='Backend for managing client projects',
            status='active',
        )
        self.other_project = ProjectFactory(
            organization=self.other_org,
            created_by=self.other_user,
            title='Other Org Project',
            description='Should not appear',
            status='active',
        )

        TaskFactory(project=self.project, title='First task', description='Completed task', completed=True)
        TaskFactory(project=self.project, title='Second task', description='Pending task', completed=False)

        self.client.force_authenticate(user=self.user)

    def project_list_url(self, org=None):
        return reverse('project-list-create', kwargs={'org_slug': (org or self.org).slug})

    def test_authenticated_member_can_list_org_projects(self):
        response = self.client.get(self.project_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Client Portal Updated')

    def test_project_response_includes_task_stats(self):
        response = self.client.get(self.project_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['total_tasks'], 2)
        self.assertEqual(response.data[0]['completed_tasks'], 1)
        self.assertEqual(response.data[0]['pending_tasks'], 1)

    def test_project_response_includes_nested_tasks(self):
        response = self.client.get(self.project_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tasks', response.data[0])
        self.assertEqual(len(response.data[0]['tasks']), 2)
        self.assertEqual(response.data[0]['tasks'][0]['project_title'], 'Client Portal Updated')

    def test_non_member_cannot_access_other_org_projects(self):
        response = self.client.get(self.project_list_url(org=self.other_org))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_project_creation_respects_plan_limit(self):
        subscription = self.org.subscription
        subscription.plan.max_projects = 1
        subscription.plan.save()

        response = self.client.post(
            self.project_list_url(), {'title': 'Second project', 'status': 'active'}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_task_creation_rejected_for_project_outside_org_membership(self):
        response = self.client.post(
            reverse('task-list-create', kwargs={'org_slug': self.org.slug}),
            {'project': self.other_project.id, 'title': 'Sneaky task'},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
