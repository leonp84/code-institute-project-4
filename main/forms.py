from django import forms
from .models import Board


class CreateBoardForm(forms.ModelForm):
    '''
    Create Django Form for users to create new Boards
    '''
    class Meta:
        model = Board
        fields = ['title', 'description']
