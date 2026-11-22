from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Task, TaskType


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="alice", password="pass12345"
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="Bug")
        self.task = Task.objects.create(
            name="Fix login", deadline=date.today(), task_type=self.task_type
        )


class LoginRequiredTests(TestCase):
    def test_pages_redirect_anonymous_users(self):
        for name in ("index", "task-list", "worker-list",
                     "position-list", "task-type-list"):
            response = self.client.get(reverse(f"task_manager:{name}"))
            self.assertEqual(response.status_code, 302)


class TaskViewTests(BaseTestCase):
    def test_toggle_completed_flips_state(self):
        url = reverse("task_manager:toggle-task-completed", args=[self.task.pk])
        self.client.post(url)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)
        self.client.post(url)
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_completed)

    def test_toggle_completed_ignores_get(self):
        url = reverse("task_manager:toggle-task-completed", args=[self.task.pk])
        self.client.get(url)
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_completed)

    def test_toggle_assign_adds_and_removes_user(self):
        url = reverse("task_manager:toggle-assign-to-task", args=[self.task.pk])
        self.client.post(url)
        self.assertIn(self.user, self.task.assignees.all())
        self.client.post(url)
        self.assertNotIn(self.user, self.task.assignees.all())

    def test_task_delete(self):
        url = reverse("task_manager:task-delete", args=[self.task.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_worker_detail_splits_completed_and_uncompleted(self):
        done = Task.objects.create(
            name="Done", deadline=date.today(),
            task_type=self.task_type, is_completed=True,
        )
        done.assignees.add(self.user)
        self.task.assignees.add(self.user)
        url = reverse("task_manager:worker-detail", args=[self.user.pk])
        response = self.client.get(url)
        self.assertEqual(list(response.context["completed_tasks"]), [done])
        self.assertEqual(list(response.context["uncompleted_tasks"]), [self.task])
