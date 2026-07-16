from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from factories import MembershipFactory, OrganizationFactory, UserFactory
from orgs.models import Membership, Organization


class RegistrationCreatesPersonalOrgTests(APITestCase):
    def test_registering_a_user_creates_a_personal_organization(self):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                reverse('register'),
                {
                    'username': 'newuser',
                    'email': 'newuser@example.com',
                    'password': 'StrongPass123!',
                },
            )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        membership = Membership.objects.get(user__username='newuser')
        self.assertEqual(membership.role, Membership.ROLE_OWNER)
        self.assertIn('newuser', membership.organization.slug)
        self.assertTrue(hasattr(membership.organization, 'subscription'))
        self.assertEqual(membership.organization.subscription.plan.name, 'free')


class OrganizationPermissionTests(APITestCase):
    def setUp(self):
        self.org = OrganizationFactory()
        self.owner = UserFactory()
        self.member = UserFactory()
        self.outsider = UserFactory()

        MembershipFactory(organization=self.org, user=self.owner, role=Membership.ROLE_OWNER)
        MembershipFactory(organization=self.org, user=self.member, role=Membership.ROLE_MEMBER)

    def invite_url(self):
        return reverse('org-invite', kwargs={'org_slug': self.org.slug})

    def test_owner_can_invite_members(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.invite_url(), {'email': self.outsider.email})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Membership.objects.filter(organization=self.org, user=self.outsider).exists()
        )

    def test_plain_member_cannot_invite(self):
        self.client.force_authenticate(user=self.member)
        response = self.client.post(self.invite_url(), {'email': self.outsider.email})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_member_cannot_view_org(self):
        self.client.force_authenticate(user=self.outsider)
        response = self.client.get(reverse('org-detail', kwargs={'org_slug': self.org.slug}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_nonexistent_org_slug_is_denied_without_leaking_existence(self):
        # A non-member gets the same 403 whether the org exists or not, so slug
        # guessing can't be used to enumerate which organizations exist.
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(reverse('org-detail', kwargs={'org_slug': 'does-not-exist'}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invite_requires_existing_account(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.invite_url(), {'email': 'ghost@example.com'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_orgs_only_returns_my_orgs(self):
        other_org = OrganizationFactory()

        self.client.force_authenticate(user=self.owner)
        response = self.client.get(reverse('org-list-create'))

        slugs = [org['slug'] for org in response.data]
        self.assertIn(self.org.slug, slugs)
        self.assertNotIn(other_org.slug, slugs)

    def test_create_org_makes_creator_owner(self):
        self.client.force_authenticate(user=self.outsider)
        response = self.client.post(reverse('org-list-create'), {'name': 'Brand New Org'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        org = Organization.objects.get(slug=response.data['slug'])
        membership = Membership.objects.get(organization=org, user=self.outsider)
        self.assertEqual(membership.role, Membership.ROLE_OWNER)
