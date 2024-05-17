from django.db import models
from main.models import Label, Column


class Task(models.Model):
    '''
    Stores a task and connects it to one specific
    Column instance at :model:`main.Column`, which in turn is connected
    to one specific Board instance at :model:`main.Board`
    '''
    title = models.CharField(max_length=255, blank=False, unique=False)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    column = models.ForeignKey(Column, on_delete=models.CASCADE,
                               related_name="task_to_column")
    column_position = models.IntegerField(default=0)
    label = models.ManyToManyField(Label)
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(null=True, blank=True)

    class Meta():
        ordering = ["id"]

    def board_name(self):
        return self.column.board.title

    def total_subtasks(self):
        return self.subtask_to_task.all().count()

    def subtasks_completed(self):
        subtasks_done = 0
        for subtask in self.subtask_to_task.all():
            if subtask.status:
                subtasks_done += 1
        return subtasks_done

    def __str__(self):
        return self.title


class Subtask(models.Model):
    '''
    Stores a subtask and connects it to one specific
    Task instance at :model:`task.Task`, which in turn is connected
    to one specific Column instance at :model:`main.Column`
    '''
    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             related_name="subtask_to_task")
    title = models.CharField(blank=False, unique=False, max_length=255)
    status = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(null=True)

    def __str__(self):
        return self.title
