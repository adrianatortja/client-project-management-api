from django.contrib import admin

from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'created_by', 'status', 'created_at')
    list_filter = ('status', 'organization')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'completed', 'created_at')
    list_filter = ('completed',)
