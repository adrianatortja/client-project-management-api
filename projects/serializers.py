from rest_framework import serializers
from .models import Project, Task


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'project', 'title', 'description', 'completed', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_project(self, value):
        request = self.context.get('request')

        if value.user != request.user:
            raise serializers.ValidationError("You can only add tasks to your own projects.")

        return value