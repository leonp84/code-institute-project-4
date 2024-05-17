from django.apps import AppConfig


class MainConfig(AppConfig):
    '''
    Configuration for the 'main' app. This app deals with Board, Column and
    Label creation, as well as User login, signup and logout.
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
