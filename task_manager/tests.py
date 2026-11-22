from datetime import timedelta, date

from django.test import TestCase
from django.urls import reverse
from task_manager.models import Position, TaskType, Task
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager


def test_task_is_overdue(self):
    task = Task.objects.create(
        name="Old", deadline=date.today() - timedelta(days=1),
        task_type=self.task_type,
    )
    self.assertTrue(task.is_overdue)

def test_completed_task_is_not_overdue(self):
    task = Task.objects.create(
        name="Old done", deadline=date.today() - timedelta(days=1),
        task_type=self.task_type, is_completed=True,
    )
    self.assertFalse(task.is_overdue)

def test_position_search(self):
    dev = Position.objects.create(name="Developer")
    Position.objects.create(name="Designer")
    response = self.client.get(
        reverse("task_manager:position-list"), {"name": "dev"}
    )
    self.assertEqual(list(response.context["position_list"]), [dev])

def test_task_type_search(self):
    bug = TaskType.objects.create(name="Bug")
    TaskType.objects.create(name="Refactoring")
    response = self.client.get(
        reverse("task_manager:task-type-list"), {"name": "bu"}
    )
    self.assertEqual(list(response.context["tasktype_list"]), [bug])
