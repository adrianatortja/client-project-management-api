import stripe
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from orgs.models import Organization
from orgs.permissions import IsOrgAdminOrOwner, IsOrgMember, OrgContextMixin

from .models import Plan, Subscription
from .serializers import SubscriptionSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


def _field(obj, key, default=None):
    """Stripe event objects support `obj['key']` but not `.get()` - normalize access."""
    try:
        return obj[key]
    except (KeyError, AttributeError, TypeError):
        return default


class SubscriptionDetailView(OrgContextMixin, generics.RetrieveAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrgMember]

    def get_object(self):
        return self.get_organization().subscription


class CreateCheckoutSessionView(OrgContextMixin, APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrgAdminOrOwner]

    def post(self, request, *args, **kwargs):
        organization = self.get_organization()
        subscription = organization.subscription

        if not settings.STRIPE_PRO_PRICE_ID:
            raise ValidationError('Stripe is not configured on this server yet.')

        session = stripe.checkout.Session.create(
            mode='subscription',
            payment_method_types=['card'],
            line_items=[{'price': settings.STRIPE_PRO_PRICE_ID, 'quantity': 1}],
            customer=subscription.stripe_customer_id or None,
            client_reference_id=organization.slug,
            success_url=f'{settings.FRONTEND_URL}/orgs/{organization.slug}/billing?checkout=success',
            cancel_url=f'{settings.FRONTEND_URL}/orgs/{organization.slug}/billing?checkout=cancel',
        )
        return Response({'checkout_url': session.url})


class CreatePortalSessionView(OrgContextMixin, APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrgAdminOrOwner]

    def post(self, request, *args, **kwargs):
        organization = self.get_organization()
        subscription = organization.subscription

        if not subscription.stripe_customer_id:
            raise ValidationError('This organization has no billing account yet.')

        session = stripe.billing_portal.Session.create(
            customer=subscription.stripe_customer_id,
            return_url=f'{settings.FRONTEND_URL}/orgs/{organization.slug}/billing',
        )
        return Response({'portal_url': session.url})


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except (ValueError, stripe.error.SignatureVerificationError):
            return Response(status=400)

        handler = getattr(self, f"_handle_{event['type'].replace('.', '_')}", None)
        if handler:
            handler(event['data']['object'])

        return Response(status=200)

    def _handle_checkout_session_completed(self, session):
        org_slug = _field(session, 'client_reference_id')
        if not org_slug:
            return

        try:
            organization = Organization.objects.get(slug=org_slug)
        except Organization.DoesNotExist:
            return

        pro_plan, _ = Plan.objects.get_or_create(
            name=Plan.PRO, defaults={'stripe_price_id': settings.STRIPE_PRO_PRICE_ID}
        )
        subscription = organization.subscription
        subscription.plan = pro_plan
        subscription.stripe_customer_id = _field(
            session, 'customer', subscription.stripe_customer_id
        )
        subscription.stripe_subscription_id = _field(session, 'subscription', '')
        subscription.status = Subscription.STATUS_ACTIVE
        subscription.save()

    def _handle_customer_subscription_updated(self, stripe_subscription):
        self._sync_subscription(stripe_subscription)

    def _handle_customer_subscription_deleted(self, stripe_subscription):
        try:
            subscription = Subscription.objects.get(
                stripe_subscription_id=_field(stripe_subscription, 'id')
            )
        except Subscription.DoesNotExist:
            return

        free_plan, _ = Plan.objects.get_or_create(
            name=Plan.FREE, defaults={'max_projects': 3}
        )
        subscription.plan = free_plan
        subscription.status = Subscription.STATUS_CANCELED
        subscription.stripe_subscription_id = ''
        subscription.save()

    def _sync_subscription(self, stripe_subscription):
        try:
            subscription = Subscription.objects.get(
                stripe_subscription_id=_field(stripe_subscription, 'id')
            )
        except Subscription.DoesNotExist:
            return

        status_map = {
            'active': Subscription.STATUS_ACTIVE,
            'trialing': Subscription.STATUS_ACTIVE,
            'past_due': Subscription.STATUS_PAST_DUE,
            'canceled': Subscription.STATUS_CANCELED,
            'unpaid': Subscription.STATUS_PAST_DUE,
        }
        subscription.status = status_map.get(
            _field(stripe_subscription, 'status'), subscription.status
        )

        period_end = _field(stripe_subscription, 'current_period_end')
        if period_end:
            subscription.current_period_end = timezone.datetime.fromtimestamp(
                period_end, tz=timezone.get_current_timezone()
            )
        subscription.save()
