from rest_framework import serializers
from .models import Project, Task


class TaskSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'project',
            'project_title',
            'title',
            'description',
            'completed',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_project(self, value):
        request = self.context.get('request')

        if value.user != request.user:
            raise serializers.ValidationError("You can only add tasks to your own projects.")

        return value


class ProjectSerializer(serializers.ModelSerializer):
    total_tasks = serializers.SerializerMethodField()
    completed_tasks = serializers.SerializerMethodField()
    pending_tasks = serializers.SerializerMethodField()
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'status',
            'created_at',
            'total_tasks',
            'completed_tasks',
            'pending_tasks',
            'tasks',
        ]
        read_only_fields = ['id', 'created_at']

    def get_total_tasks(self, obj):
        return obj.tasks.count()

    def get_completed_tasks(self, obj):
        return obj.tasks.filter(completed=True).count()

    def get_pending_tasks(self, obj):
        return obj.tasks.filter(completed=False).count()
    