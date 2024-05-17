from django.apps import AppConfig


class TaskConfig(AppConfig):
    '''
    Configuration for the 'task' app. This app deals with task and subtask
    creation and positioning within the correct columns and boards.
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task'
