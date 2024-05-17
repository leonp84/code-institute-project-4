from django.apps import AppConfig


class MainConfig(AppConfig):
    '''
    Configuration for the 'main' app. This app deals with board, column and
    label creation, as well as user login, signup and logout.
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
