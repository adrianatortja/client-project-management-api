from django.db.models import Count, Q
from rest_framework import generics, permissions, filters
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from orgs.permissions import IsOrgMember, OrgContextMixin

from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer


def _annotate_task_counts(queryset):
    return queryset.annotate(
        total_tasks_count=Count('tasks', distinct=True),
        completed_tasks_count=Count('tasks', filter=Q(tasks__completed=True), distinct=True),
        pending_tasks_count=Count('tasks', filter=Q(tasks__completed=False), distinct=True),
    )


class ProjectListCreateView(OrgContextMixin, generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrgMember]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['title']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        return _annotate_task_counts(
            Project.objects.filter(organization=self.get_organization())
        )

    def perform_create(self, serializer):
        organization = self.get_organization()
        max_projects = organization.subscription.plan.max_projects

        if max_projects is not None and organization.projects.count() >= max_projects:
            raise ValidationError(
                f"You've reached the {max_projects}-project limit for your plan. "
                "Upgrade to add more."
            )

        serializer.save(organization=organization, created_by=self.request.user)


class ProjectDetailView(OrgContextMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrgMember]

    def get_queryset(self):
        return _annotate_task_counts(
            Project.objects.filter(organization=self.get_organization())
        )


class TaskListCreateView(OrgContextMixin, generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrgMember]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['completed']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at', '-id']

    def get_queryset(self):
        return Task.objects.filter(project__organization=self.get_organization())

    def perform_create(self, serializer):
        serializer.save()


class TaskDetailView(OrgContextMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrgMember]

    def get_queryset(self):
        return Task.objects.filter(project__organization=self.get_organization())
