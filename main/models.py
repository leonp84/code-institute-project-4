from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="boards")
    title = models.CharField(max_length=200, blank=False, unique=True)
    description = models.TextField(blank=True)
    has_archived_tasks = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


class Column(models.Model):
    title = models.CharField(max_length=50, blank=False)
    colour = models.CharField(default='white')
    board = models.ForeignKey(Board, on_delete=models.CASCADE,
                              related_name="column_to_board")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


class Label(models.Model):
    title = models.CharField(max_length=20, blank=False)
    colour = models.CharField(default='light')
    board = models.ForeignKey(Board, on_delete=models.CASCADE,
                              related_name="label_to_board")

    def __str__(self):
        return f"*{self.title}* OF BOARD: {self.board}"


class Task(models.Model):
    title = models.CharField(max_length=300, blank=False, unique=True)
    description = models.TextField(blank=True)
    priority = models.CharField()
    status = models.CharField()
    completed = models.BooleanField(default=False)
    label = models.ManyToManyField(Label)
    column = models.ForeignKey(Column, on_delete=models.CASCADE,
                               related_name="task_to_column")
    archived = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(blank=True)

    def total_subtasks(self):
        return self.subtask_to_task.all().count()

    def subtasks_completed(self):
        subtasks_done = 0
        for subtask in self.subtask_to_task.all():
            if subtask.status:
                subtasks_done += 1
        return subtasks_done

    def __str__(self):
        return f"*{self.title}* ON COLUMN: {self.column}"


class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             related_name="subtask_to_task")
    title = models.CharField(max_length=300, blank=False, unique=True)
    status = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(blank=True)

    def __str__(self):
        return f"*{self.title}* OF TASK: {self.task}"
