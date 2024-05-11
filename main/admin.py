from django.contrib import admin
from .models import Board, Column, Label, Task, Subtask

admin.site.register(Board)
admin.site.register(Column)
admin.site.register(Label)
admin.site.register(Task)
admin.site.register(Subtask)
