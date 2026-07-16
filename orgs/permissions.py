from django.shortcuts import get_object_or_404
from rest_framework import permissions

from .models import Membership, Organization


class OrgContextMixin:
    """Resolves the `organization` from `org_slug` in the URL kwargs."""

    def get_organization(self):
        return get_object_or_404(Organization, slug=self.kwargs['org_slug'])

    def get_membership(self):
        return get_object_or_404(
            Membership, organization=self.get_organization(), user=self.request.user
        )


class IsOrgMember(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return Membership.objects.filter(
            organization__slug=view.kwargs.get('org_slug'), user=request.user
        ).exists()


class IsOrgAdminOrOwner(IsOrgMember):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return Membership.objects.filter(
            organization__slug=view.kwargs.get('org_slug'),
            user=request.user,
            role__in=[Membership.ROLE_OWNER, Membership.ROLE_ADMIN],
        ).exists()
