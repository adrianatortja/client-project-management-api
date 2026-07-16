from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Membership, Organization
from .utils import unique_org_slug


@receiver(post_save, sender=get_user_model())
def create_personal_organization(sender, instance, created, **kwargs):
    if not created:
        return

    def _create():
        org = Organization.objects.create(
            name=f"{instance.username}'s Organization",
            slug=unique_org_slug(instance.username),
        )
        Membership.objects.create(
            organization=org, user=instance, role=Membership.ROLE_OWNER
        )

    transaction.on_commit(_create)
