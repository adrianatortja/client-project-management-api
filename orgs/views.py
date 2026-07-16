from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Membership, Organization
from .permissions import IsOrgAdminOrOwner, IsOrgMember, OrgContextMixin
from .serializers import InviteSerializer, MembershipSerializer, OrganizationSerializer

User = get_user_model()


class OrganizationListCreateView(generics.ListCreateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Organization.objects.filter(memberships__user=self.request.user)

    def perform_create(self, serializer):
        with transaction.atomic():
            org = serializer.save()
            Membership.objects.create(
                organization=org, user=self.request.user, role=Membership.ROLE_OWNER
            )


class OrganizationDetailView(OrgContextMixin, generics.RetrieveAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrgMember]
    lookup_field = 'slug'
    lookup_url_kwarg = 'org_slug'

    def get_queryset(self):
        return Organization.objects.all()


class MembershipListView(OrgContextMixin, generics.ListAPIView):
    serializer_class = MembershipSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrgMember]

    def get_queryset(self):
        return Membership.objects.filter(organization=self.get_organization())


class MembershipInviteView(OrgContextMixin, APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrgAdminOrOwner]

    def post(self, request, *args, **kwargs):
        serializer = InviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization = self.get_organization()
        user = User.objects.get(email=serializer.validated_data['email'])

        if Membership.objects.filter(organization=organization, user=user).exists():
            raise ValidationError('This user is already a member of the organization.')

        membership = Membership.objects.create(
            organization=organization,
            user=user,
            role=serializer.validated_data['role'],
        )
        return Response(
            MembershipSerializer(membership).data, status=201
        )
