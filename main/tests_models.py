from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime
from .models import Column, Board, Label


class TestBoardModel(TestCase):
    '''
    Test board modal functionality.
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
            has_archived_tasks=False,
            created_on=datetime.now(),
        )
        self.board.save()

    def test_board_creation(self):
        self.assertEqual(self.board.title, 'Test Board')
        self.assertEqual(self.board.description, 'Test Board Description')
        self.assertFalse(self.board.has_archived_tasks)
        self.assertIsNotNone(self.board.created_on)


class TestColumnModel(TestCase):
    '''
    Test column modal functionality.
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

    def test_column_creation(self):
        self.assertEqual(self.column.title, 'test column')
        self.assertEqual(self.column.colour, 'red')
        self.assertEqual(self.column.board, self.board)


class TestLabelModel(TestCase):
    '''
    Test label modal functionality.
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

        self.label = Label(
            title='test label',
            colour='red',
            board=self.board,
        )
        self.label.save()

    def test_label_creation(self):
        self.assertEqual(self.label.title, 'test label')
        self.assertEqual(self.label.colour, 'red')
        self.assertEqual(self.board, self.board)
