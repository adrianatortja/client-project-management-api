import hashlib
import hmac
import json
import time
from unittest.mock import MagicMock, patch

from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from factories import MembershipFactory, OrganizationFactory, SubscriptionFactory, UserFactory
from billing.models import Plan, Subscription
from orgs.models import Membership

WEBHOOK_SECRET = 'whsec_test_secret'


def sign_payload(payload: bytes, secret: str) -> str:
    timestamp = int(time.time())
    signed_payload = f'{timestamp}.{payload.decode()}'
    signature = hmac.new(secret.encode(), signed_payload.encode(), hashlib.sha256).hexdigest()
    return f't={timestamp},v1={signature}'


class CheckoutSessionTests(APITestCase):
    def setUp(self):
        self.org = OrganizationFactory()
        self.owner = UserFactory()
        MembershipFactory(organization=self.org, user=self.owner, role=Membership.ROLE_OWNER)
        SubscriptionFactory(organization=self.org)

    def checkout_url(self):
        return reverse('billing-checkout', kwargs={'org_slug': self.org.slug})

    def test_checkout_requires_stripe_price_configured(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.checkout_url())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(STRIPE_PRO_PRICE_ID='price_123')
    @patch('billing.views.stripe.checkout.Session.create')
    def test_checkout_creates_session_when_configured(self, mock_create):
        mock_create.return_value = MagicMock(url='https://checkout.stripe.com/test-session')

        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.checkout_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['checkout_url'], 'https://checkout.stripe.com/test-session')
        mock_create.assert_called_once()


@override_settings(STRIPE_WEBHOOK_SECRET=WEBHOOK_SECRET)
class StripeWebhookTests(APITestCase):
    def setUp(self):
        self.org = OrganizationFactory()
        self.subscription = SubscriptionFactory(organization=self.org)

    def webhook_url(self):
        return reverse('stripe-webhook')

    def post_event(self, event, secret=WEBHOOK_SECRET):
        event = {'id': 'evt_test', 'object': 'event', **event}
        payload = json.dumps(event).encode()
        signature = sign_payload(payload, secret)
        return self.client.post(
            self.webhook_url(),
            data=payload,
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE=signature,
        )

    def test_rejects_invalid_signature(self):
        event = {'type': 'checkout.session.completed', 'data': {'object': {}}}
        response = self.post_event(event, secret='wrong_secret')

        self.assertEqual(response.status_code, 400)

    def test_checkout_completed_upgrades_org_to_pro(self):
        event = {
            'type': 'checkout.session.completed',
            'data': {
                'object': {
                    'client_reference_id': self.org.slug,
                    'customer': 'cus_123',
                    'subscription': 'sub_123',
                }
            },
        }
        response = self.post_event(event)

        self.assertEqual(response.status_code, 200)
        self.subscription.refresh_from_db()
        self.assertEqual(self.subscription.plan.name, Plan.PRO)
        self.assertEqual(self.subscription.stripe_customer_id, 'cus_123')
        self.assertEqual(self.subscription.status, Subscription.STATUS_ACTIVE)

    def test_subscription_deleted_downgrades_to_free(self):
        self.subscription.stripe_subscription_id = 'sub_123'
        pro_plan, _ = Plan.objects.get_or_create(name=Plan.PRO)
        self.subscription.plan = pro_plan
        self.subscription.save()

        event = {
            'type': 'customer.subscription.deleted',
            'data': {'object': {'id': 'sub_123'}},
        }
        response = self.post_event(event)

        self.assertEqual(response.status_code, 200)
        self.subscription.refresh_from_db()
        self.assertEqual(self.subscription.plan.name, Plan.FREE)
        self.assertEqual(self.subscription.status, Subscription.STATUS_CANCELED)
