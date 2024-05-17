from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from django.test import Client
from main.models import Board, Column, Label


class TestNewTaskCreation(TestCase):
    '''
    Test task creation process functionality, populating a reloaded version
    of the main landing page with a new instance Task.
    '''
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

    def test_successful_task_creation(self):

        self.client = Client()
        self.client.login(username="myUsername", password="myPassword")

        new_task = {
            'title': 'New Test Task',
            'description': 'New Test Task Description',
            'priority': 'red',
            'status': Column.objects.all().first().id
        }

        self.client.post(reverse(
            'add_new_task', args=[self.board.id]), new_task)
        response = self.client.get(reverse('show_board', args=[self.board.id]))

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Test Task', response.content)
