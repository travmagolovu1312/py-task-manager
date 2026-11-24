from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from task_manager.models import Position, Task, TaskType, Tag


class ModelTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.task_type = TaskType.objects.create(name="Bug")
        self.worker = get_user_model().objects.create_user(
            username="alice", password="pass12345",
            first_name="Alice", last_name="Smith", position=self.position,
        )

    def test_position_str(self):
        self.assertEqual(str(self.position), "Developer")

    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), "Bug")

    def test_worker_str(self):
        self.assertEqual(str(self.worker), "alice (Alice Smith)")

    def test_task_defaults(self):
        task = Task.objects.create(
            name="Fix login", deadline=date.today() + timedelta(days=3),
            task_type=self.task_type,
        )
        self.assertFalse(task.is_completed)
        self.assertEqual(task.priority, Task.Priority.MEDIUM)
        self.assertEqual(str(task), "Fix login")

    def test_task_assignees_many_to_many(self):
        task = Task.objects.create(
            name="Fix login", deadline=date.today(), task_type=self.task_type
        )
        task.assignees.add(self.worker)
        self.assertIn(task, self.worker.tasks.all())

    def test_tag_str(self):
        self.assertEqual(str(Tag.objects.create(name="python")), "python")

    def test_task_tags_many_to_many(self):
        tag = Tag.objects.create(name="python")
        task = Task.objects.create(
            name="Refactor", deadline=date.today(), task_type=self.task_type
        )
        task.tags.add(tag)
        self.assertIn(task, tag.tasks.all())
