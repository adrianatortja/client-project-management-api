from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from orgs.models import Organization

from .models import Plan, Subscription


@receiver(post_save, sender=Organization)
def create_free_subscription(sender, instance, created, **kwargs):
    if not created:
        return

    def _create():
        free_plan, _ = Plan.objects.get_or_create(
            name=Plan.FREE, defaults={'max_projects': 3}
        )
        Subscription.objects.get_or_create(
            organization=instance, defaults={'plan': free_plan}
        )

    transaction.on_commit(_create)
