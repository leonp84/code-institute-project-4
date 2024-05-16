from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .models import Board, Column
from task.models import Task, Subtask, Label
from datetime import datetime
from django.test import Client


class TestLandingPage(TestCase):
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

        self.label = Label(
            title='test label',
            colour='red',
            board=self.board,
        )
        self.label.save()

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

    def test_render_show_board_view_with_new_board(self):

        self.client = Client()
        self.client.login(username="myUsername", password="myPassword")

        response = self.client.get(reverse('show_board', args=[self.board.id]))

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Board', response.content)
        self.assertIn(b'test column', response.content)
        self.assertIn(b'test label', response.content)
        self.assertIn(b'Test Task', response.content)
        self.assertIn(b'Test Subtask', response.content)
        self.assertIsInstance(response.context['board'], Board)
