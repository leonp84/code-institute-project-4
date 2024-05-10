from .models import Board, Task
from django import forms


class CreateBoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'description']


class CreateNewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status']
