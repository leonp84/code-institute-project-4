from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="board_to_user")
    title = models.CharField(max_length=200, blank=False, unique=False)
    description = models.TextField(blank=True)
    has_archived_tasks = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


class Column(models.Model):
    title = models.CharField(max_length=50, blank=False, unique=False)
    colour = models.CharField(default='white')
    board = models.ForeignKey(Board, on_delete=models.CASCADE,
                              related_name="column_to_board")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


class Label(models.Model):
    title = models.CharField(max_length=20, blank=False, unique=False)
    colour = models.CharField(default='light')
    board = models.ForeignKey(Board, on_delete=models.CASCADE,
                              related_name="label_to_board")

    def __str__(self):
        return f"*{self.title}* OF BOARD: {self.board}"
