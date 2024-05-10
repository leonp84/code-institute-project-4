from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="boards")
    title = models.CharField(max_length=200, blank=False, unique=True)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"{self.title} | Owner: {self.author}"


class Column(models.Model):
    title = models.CharField(max_length=200, blank=False)
    colour = models.CharField(default='white')
    board = models.ForeignKey(Board, on_delete=models.CASCADE,
                              related_name="board_to_column")

    def __str__(self):
        return f"{self.title} on board: {self.board}"


class Label(models.Model):
    title = models.CharField(max_length=200, blank=False)
    colour = models.CharField(default='white')
    board = models.ForeignKey(Board, on_delete=models.CASCADE,
                              related_name="label_to_board")

    def __str__(self):
        return f"{self.title} on board: {self.board}"


class Task(models.Model):
    title = models.CharField(max_length=200, blank=False, unique=True)
    description = models.TextField(blank=True)
    priority = models.CharField()
    status = models.CharField()
    label = models.ManyToManyField('Label')
    column = models.ForeignKey(Column, on_delete=models.CASCADE,
                               related_name="task_to_column")
    archived = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} on column: {self.column}"
