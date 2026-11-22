from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Task, TaskType


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="alice", password="pass12345"
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="Bug")

    def _task(self, name):
        return Task.objects.create(
            name=name, deadline=date.today(), task_type=self.task_type
        )

    def test_task_search_includes_match_and_excludes_other(self):
        match = self._task("Fix login page")
        self._task("Update docs")
        response = self.client.get(reverse("task_manager:task-list"), {"name": "login"})
        self.assertEqual(list(response.context["task_list"]), [match])

    def test_task_search_is_case_insensitive(self):
        match = self._task("Fix login page")
        response = self.client.get(reverse("task_manager:task-list"), {"name": "LOGIN"})
        self.assertEqual(list(response.context["task_list"]), [match])

    def test_empty_search_returns_all(self):
        self._task("One")
        self._task("Two")
        response = self.client.get(reverse("task_manager:task-list"), {"name": ""})
        self.assertEqual(len(response.context["task_list"]), 2)

    def test_worker_search_by_username(self):
        bob = get_user_model().objects.create_user(username="bob", password="pass12345")
        response = self.client.get(reverse("task_manager:worker-list"), {"username": "bo"})
        self.assertEqual(list(response.context["worker_list"]), [bob])

    def test_pagination_keeps_search_query(self):
        for i in range(6):
            self._task(f"Report {i}")
        response = self.client.get(reverse("task_manager:task-list"), {"name": "Report"})
        self.assertContains(response, "page=2")
        self.assertContains(response, "name=Report")
