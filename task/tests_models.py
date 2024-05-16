from django.test import TestCase
from .models import Task, Subtask
from main.models import Column, Board
from django.contrib.auth.models import User
from datetime import datetime


# Create your tests here.
class TestTaskModel(TestCase):
    def setUp(self):

        self.user = User.objects.create_superuser(
            username="myUsername",
            password="myPassword",
            email="test@test.com"
        )

        self.board = Board(
            author=self.user,
            title='Test Board',
            description='Test Board Description',
        )
        self.board.save()

        self.column = Column(
            title='test column',
            colour='red',
            board=self.board,
        )
        self.column.save()

        self.task = Task(
            title='Test Task',
            description='Test Task Description',
            priority='red',
            status='37',
            completed=False,
            archived=False,
            column=self.column,
            created_on=datetime.now(),
            completed_on=None,
        )
        self.task.save()

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'Test Task Description')
        self.assertEqual(self.task.priority, 'red')
        self.assertEqual(self.task.status, '37')
        self.assertEqual(self.task.completed, False)
        self.assertFalse(self.task.archived)
        self.assertIsNotNone(self.task.created_on)
        self.assertIsNone(self.task.completed_on)


class TestSubaskModel(TestCase):
    def setUp(self):

        self.user = User.objects.create_superuser(
            username="myUsername",
            password="myPassword",
            email="test@test.com"
        )

        self.board = Board(
            author=self.user,
            title='Test Board',
            description='Test Board Description',
        )
        self.board.save()

        self.column = Column(
            title='test column',
            colour='red',
            board=self.board,
        )
        self.column.save()

        self.task = Task(
            title='Test Task',
            description='Test Task Description',
            priority='red',
            status='37',
            column=self.column,
        )
        self.task.save()

        self.subtask = Subtask(
            task=self.task,
            title='Test Subtask',
            status=False,
            created_on=datetime.now(),
            completed_on=None,
        )
        self.subtask.save()

    def test_subtask_creation(self):
        self.assertEqual(self.subtask.task, self.task)
        self.assertEqual(self.subtask.title, 'Test Subtask')
        self.assertFalse(self.subtask.status)
        self.assertIsNotNone(self.subtask.created_on)
        self.assertIsNone(self.subtask.completed_on)
