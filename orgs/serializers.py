from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Membership, Organization
from .utils import unique_org_slug

User = get_user_model()


class OrganizationSerializer(serializers.ModelSerializer):
    my_role = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ['id', 'name', 'slug', 'created_at', 'my_role', 'member_count']
        read_only_fields = ['id', 'slug', 'created_at']

    def get_my_role(self, obj):
        request = self.context.get('request')
        membership = obj.memberships.filter(user=request.user).first()
        return membership.role if membership else None

    def get_member_count(self, obj):
        return obj.memberships.count()

    def create(self, validated_data):
        validated_data['slug'] = unique_org_slug(validated_data['name'])
        return super().create(validated_data)


class MembershipSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Membership
        fields = ['id', 'username', 'email', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']


class InviteSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(
        choices=[Membership.ROLE_ADMIN, Membership.ROLE_MEMBER],
        default=Membership.ROLE_MEMBER,
    )

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'No account exists with this email yet. Ask them to register first.'
            )
        return value
