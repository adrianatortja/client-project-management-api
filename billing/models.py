from django.db import models

from orgs.models import Organization


class Plan(models.Model):
    FREE = 'free'
    PRO = 'pro'
    NAME_CHOICES = [
        (FREE, 'Free'),
        (PRO, 'Pro'),
    ]

    name = models.CharField(max_length=50, choices=NAME_CHOICES, unique=True)
    stripe_price_id = models.CharField(max_length=255, blank=True)
    max_projects = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.get_name_display()


class Subscription(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_PAST_DUE = 'past_due'
    STATUS_CANCELED = 'canceled'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_PAST_DUE, 'Past due'),
        (STATUS_CANCELED, 'Canceled'),
    ]

    organization = models.OneToOneField(
        Organization, on_delete=models.CASCADE, related_name='subscription'
    )
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    current_period_end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.organization} - {self.plan}'
