from django import forms
from .models import Task


class CreateNewTaskForm(forms.ModelForm):
    '''
    Create Django Form for users to create new Tasks
    '''
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status']
