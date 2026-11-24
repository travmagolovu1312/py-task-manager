from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_manager.models import Position, Task, TaskType, Worker, Tag

@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("position",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("first_name", "last_name",
                                    "position")}),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "task_type",
        "priority",
        "deadline",
        "is_completed"
    )
    list_filter = (
        "task_type",
        "priority",
        "is_completed",
    )
    search_fields = ("name",)

admin.site.register(Tag)
admin.site.register(TaskType)
