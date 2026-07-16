from rest_framework import serializers

from .models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = serializers.CharField(source='plan.name', read_only=True)
    max_projects = serializers.IntegerField(source='plan.max_projects', read_only=True)

    class Meta:
        model = Subscription
        fields = ['plan', 'max_projects', 'status', 'current_period_end']
