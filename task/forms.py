from .models import Task
from django import forms


class CreateNewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status']
