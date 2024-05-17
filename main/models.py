from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    '''
    Stores a kanban board and connects it to a single user account
    at :model:`auth.User`.
    '''
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="board_to_user")
    title = models.CharField(max_length=255, blank=False, unique=False)
    description = models.TextField(blank=True)
    has_archived_tasks = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


class Column(models.Model):
    '''
    Stores a single column within a board and connects it to one specific
    Board instance at :model:`main.Board`.
    '''
    title = models.CharField(blank=False, unique=False, max_length=255)
    colour = models.CharField(default='white', max_length=255)
    board = models.ForeignKey(Board, on_delete=models.CASCADE,
                              related_name="column_to_board")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


class Label(models.Model):
    '''
    Stores a label within a board and connects it to one specific
    Board instance at :model:`main.Board`.
    '''
    title = models.CharField(blank=False, unique=False, max_length=255)
    colour = models.CharField(default='light', max_length=255)
    board = models.ForeignKey(Board, on_delete=models.CASCADE,
                              related_name="label_to_board")

    def __str__(self):
        return f"*{self.title}* OF BOARD: {self.board}"
