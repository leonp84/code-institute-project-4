from django.test import TestCase
from .forms import CreateNewTaskForm


class TestCreateNewTaskForm(TestCase):

    def test_create_new_task_form_is_valid(self):
        new_task = CreateNewTaskForm({
            'title': 'test task',
            'description': 'test task description',
            'priority': 'red',
            'status': '37',
            })
        self.assertTrue(new_task.is_valid())
