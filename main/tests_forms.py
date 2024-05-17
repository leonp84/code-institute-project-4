from django.test import TestCase
from .forms import CreateBoardForm


class TestCreateBoardForm(TestCase):
    '''
    Test board creation form functionality.
    '''
    def test_create_new_board_form_is_valid(self):
        new_board = CreateBoardForm({
            'title': 'test board',
            'description': 'test board description',
            })
        self.assertTrue(new_board.is_valid())
